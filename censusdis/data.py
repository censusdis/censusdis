from abc import ABC, abstractmethod
from collections import defaultdict
from typing import (
    Any,
    DefaultDict,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

import pandas as pd
import requests

import censusdis.geography as cgeo

# This is the type we can accept for geographic
# filters. When provided, these filters are either
# single values as a string, or, if multivalued,
# then an iterable containing all the values allowed
# by the filter.
GeoFilterType = Optional[Union[str, Iterable[str]]]


def _gf2s(geo_filter: GeoFilterType) -> Optional[str]:
    """
    Utility to convert a filter to a string.

    For the Census API, multiple values are encoded
    in a single comma separated string.
    """
    if geo_filter is None or isinstance(geo_filter, str):
        return geo_filter
    return ",".join(geo_filter)


class CensusApiException(Exception):
    pass


def data_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> pd.DataFrame:
    parsed_json = json_from_url(url, params)
    if (
        isinstance(parsed_json, list)
        and len(parsed_json) >= 1
        and isinstance(parsed_json[0], list)
    ):
        return pd.DataFrame(
            parsed_json[1:],
            columns=(
                c.upper()
                .replace(" ", "_")
                .replace("-", "_")
                .replace("/", "_")
                .replace("(", "")
                .replace(")", "")
                for c in parsed_json[0]
            ),
        )

    raise CensusApiException(
        f"Expected json data to be a list of lists, not a {type(parsed_json)}"
    )


def json_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> Any:
    request = requests.get(url, params=params)

    if request.status_code == 200:
        parsed_json = request.json()
        return parsed_json

    # Do our best to tell the user something informative.
    raise CensusApiException(
        f"Census API request to {request.url} failed with status {request.status_code}. {request.text}"
    )


_MAX_FIELDS_PER_DOWNLOAD = 50


def _download_concat_detail(
    dataset: str,
    year: int,
    fields: List[str],
    key: Optional[str],
    census_variables: "VariableCache",
    **kwargs: cgeo.InSpecType,
) -> pd.DataFrame:

    # Divide the fields into groups.
    field_groups = [
        # black and flake8 disagree about the whitespace before ':' here...
        fields[start : start + _MAX_FIELDS_PER_DOWNLOAD]  # noqa: 203
        for start in range(0, len(fields), _MAX_FIELDS_PER_DOWNLOAD)
    ]

    # Get the data for each chunk.
    dfs = [
        download_detail(
            dataset,
            year,
            field_group,
            api_key=key,
            census_variables=census_variables,
            **kwargs,
        )
        for field_group in field_groups
    ]

    # What fields came back in the first df but were not
    # requested? These are the ones that will be duplicated
    # in the later dfs.
    extra_fields = [f for f in dfs[0].columns if f not in set(field_groups[0])]

    df_data = dfs[0]

    for df_right in dfs[1:]:
        df_data = df_data.merge(df_right, on=extra_fields)

    return df_data


def download_detail(
    dataset: str,
    year: int,
    fields: Iterable[str],
    *,
    api_key: Optional[str] = None,
    census_variables: Optional["VariableCache"] = None,
    **kwargs: cgeo.InSpecType,
) -> pd.DataFrame:
    if census_variables is None:
        census_variables = variables

    # In case they came to us in py format, as kwargs often do.
    cgeo.geo_path_snake_specs(dataset, year)
    kwargs = {
        cgeo.path_component_from_snake(dataset, year, k): v for k, v in kwargs.items()
    }

    if not isinstance(fields, list):
        fields = list(fields)

    # Special case if we are trying to get too many fields.
    if len(fields) > _MAX_FIELDS_PER_DOWNLOAD:
        return _download_concat_detail(
            dataset,
            year,
            fields,
            key=api_key,
            census_variables=census_variables,
            **kwargs,
        )

    # Prefetch all the types before we load the data.
    # That way we fail fast if a field is not known.
    for field in fields:
        census_variables.get(dataset, year, field)

    # If we were given a list, join it together into
    # a comma-separated string.
    string_kwargs = {k: _gf2s(v) for k, v in kwargs.items()}

    url, params = census_detail_table_url(
        dataset, year, fields, api_key=api_key, **string_kwargs
    )
    df_data = data_from_url(url, params)

    for field in fields:
        field_type = census_variables.get(dataset, year, field)["predicateType"]

        if field_type == "int":
            df_data[field] = df_data[field].astype(int)
        elif field_type == "float":
            df_data[field] = df_data[field].astype(float)
        elif field_type == "string":
            pass
        else:
            # Leave it as an object?
            pass

    # Put the geo fields that came back up front.
    df_data = df_data[[col for col in df_data.columns if col not in fields] + fields]

    return df_data


def census_detail_table_url(
    dataset: str,
    year: int,
    fields: Iterable[str],
    *,
    api_key: Optional[str] = None,
    **kwargs: cgeo.InSpecType,
) -> Tuple[str, Mapping[str, str]]:
    bound_path = cgeo.PathSpec.partial_prefix_match(dataset, year, **kwargs)

    if bound_path is None:
        raise CensusApiException(
            f"Unable to match the geography specification {kwargs}.\n"
            f"Supported geographies for dataset='{dataset}' in year={year} are:\n"
            + "\n".join(
                f"{path_spec}"
                for path_spec in cgeo.geo_path_snake_specs(dataset, year).values()
            )
        )

    query_spec = cgeo.CensusGeographyQuerySpec(
        dataset, year, list(fields), bound_path, api_key=api_key
    )

    url, params = query_spec.detail_table_url()

    return url, params


class VariableSource(ABC):
    """
    A source of variables, typically used behind a :py:class:`~VariableCache`.

    The purpose of this class is to get variable and group information
    from a source, typically a remote API call to the US Census API.
    Another use case is to enable mocking for testing the rest of the
    :py:class:`~VariableCache` functionality, which is a superset of
    what this class does.
    """

    @abstractmethod
    def get(
        self,
        dataset: str,
        year: int,
        name: str,
    ) -> Dict[str, Any]:
        """
        Get information on a variable for a given dataset in a given year.

        The return value is a dictionary with the following fields:

        .. list-table:: Title
            :widths: 25 75
            :header-rows: 0

        * - `"name"`
          - The name of the variable.
        * - '"label"`
          - A description of the variable. Within groups, hierarchies of
            variables are represented by seperating levels with `"!!"`.
        * - `"concept"'
          - The concept this variable and others in the group represent.
        * - `"group"`
          - The group the variable belongs to. To query an entire group,
            use the :py:meth:`~get_group` method.
        * - `"limit"`
          -
        * - `"attributes"`
          - A comma-separated list of variables that are attributes of this
            one.

        This dictionary is very much like the JSON returned from US Census
        API URLs like
        https://api.census.gov/data/2020/acs/acs5/variables/B03001_001E.json

        Parameters
        ----------
        dataset
            The census dataset, for example `dec/acs5` for ACS5 data
            (https://www.census.gov/data/developers/data-sets/acs-5year.html and
            https://api.census.gov/data/2020/acs/acs5.html)
            or `dec/pl` for redistricting data
            (https://www.census.gov/programs-surveys/decennial-census/about/rdo.html and
            https://api.census.gov/data/2020/dec/pl.html)
        year
            The year
        name
            The name of the variable to get information about. For example,
            `B03002_001E` is a variable from the ACS5 data set that represents
            total population in a geographic area.
        Returns
        -------
            A dictionary of information about the variable.
        """
        raise NotImplementedError("Abstract method.")

    @abstractmethod
    def get_group(
        self,
        dataset: str,
        year: int,
        name: str,
    ) -> Dict[str, Dict]:
        """
        Get information on a group of variables for a given dataset in a given year.

        The return value is a dictionary that is very much like the JSON returned
        from US Census API URLs like
        https://api.census.gov/data/2020/acs/acs5/groups/B03002.json

        See :py:meth:`~VariableSource.get` for more details.

        Parameters
        ----------
        dataset
            The census dataset, for example `dec/acs5` for ACS5 data
            (https://www.census.gov/data/developers/data-sets/acs-5year.html and
            https://api.census.gov/data/2020/acs/acs5.html)
            or `dec/pl` for redistricting data
            (https://www.census.gov/programs-surveys/decennial-census/about/rdo.html and
            https://api.census.gov/data/2020/dec/pl.html)
        year
            The year
        name
            The name of the group to get information about. For example,
            `B03002` is a group from the ACS5 data set that contains
            variables that represent the population of various racial and
            ethnic groups in a geographic area.

        Returns
        -------
            A dictionary with a single key `"variables"`. The value
            associated with that key is a dictionary that maps from the
            names of variables in the group to dictionaries of attributes
            of the variable, in the same form as that returned for individual
            variables by the method :py:meth:`~VariableSource.get`.
        """
        raise NotImplementedError("Abstract method.")


class CensusApiVariableSource(VariableSource):
    """
    A :py:class:`~VariableSource` that gets data from the US Census remote API.

    Users will rarely if ever need to explicitly construct objects
    of this class. There is one behind the singleton cache
    `censusdis.censusdata.variables`.
    """

    @staticmethod
    def url(
        dataset: str,
        year: int,
        name: str,
    ) -> str:
        return f"https://api.census.gov/data/{year}/{dataset}/variables/{name}.json"

    @staticmethod
    def group_url(
        dataset: str,
        year: int,
        name: str,
    ) -> str:
        return f"https://api.census.gov/data/{year}/{dataset}/groups/{name}.json"

    def get(self, dataset: str, year: int, name: str) -> Dict[str, Any]:
        url = self.url(dataset, year, name)
        value = json_from_url(url)

        return value

    def get_group(self, dataset: str, year: int, name: str) -> Dict[str, Dict]:
        url = self.group_url(dataset, year, name)
        value = json_from_url(url)

        # Put the name into the nested dictionaries, so it looks the same is if
        # we had gotten it via the variable API even though that API leaves it out.
        for k, v in value["variables"].items():
            v["name"] = k

        return value


class VariableCache:
    """
    A cache of vatiables and groups.

    This looks a lot like a :py:class:`~VariableSource` but it
    implements a cache in front of a :py:class:`~VariableSource`.

    Users will rarely if ever need to construct one of these
    themselves. In almost all cases they will use the singleton
    `censusdis.censusdata.variables`.
    """

    def __init__(self, *, variable_source: Optional[VariableSource] = None):
        if variable_source is None:
            variable_source = CensusApiVariableSource()

        self._variable_source = variable_source
        self._variable_cache: DefaultDict[
            str, DefaultDict[int, Dict[str, Any]]
        ] = defaultdict(lambda: defaultdict(dict))
        self._group_cache: DefaultDict[
            str, DefaultDict[int, Dict[str, Any]]
        ] = defaultdict(lambda: defaultdict(dict))

    def get(
        self,
        dataset: str,
        year: int,
        name: str,
    ) -> Dict[str, Dict]:
        """
        Get the description of a given variable.

        See :py:meth:`VariableSource.get`
        for details on the data format. We first look in the cache and then if
        we don't find what we are looking for, we call the source behind us and
        cache the results before returning them.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        name
            The name of the variable.

        Returns
        -------
            The details of the variable.
        """
        cached_value = self._variable_cache[dataset][year].get(name, None)

        if cached_value is not None:
            return cached_value

        value = self._variable_source.get(dataset, year, name)

        self._variable_cache[dataset][year][name] = value

        return value

    def get_group(
        self,
        dataset: str,
        year: int,
        name: str,
    ) -> Dict[str, Dict]:
        """
        Get inforation on the variables in a group.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        name
            The name of the group.

        Returns
        -------
            A dictionary that maps from the names of each variable in the group
            to a dictionary containing a description of the variable. The
            format of the description is a dictionary as described in
            the documentation for
            :py:meth:`VariableSource.get`.
        """
        group_variable_names = self._group_cache[dataset][year].get(name, None)

        if group_variable_names is None:
            # Missed in the cache, so go fetch it.
            value = self._variable_source.get_group(dataset, year, name)

            # Cache all the variables in the group.
            group_variables = value["variables"]

            for variable_name, variable_details in group_variables.items():
                self._variable_cache[dataset][year][variable_name] = variable_details

            # Cache the names of the variables in the group.
            group_variable_names = list(
                variable_name for variable_name in group_variables
            )
            self._group_cache[dataset][year][name] = group_variable_names

        # Reformat what we return so it includes the full
        # details on each variable.
        return {
            group_variable_name: self.get(dataset, year, group_variable_name)
            for group_variable_name in group_variable_names
        }

    class GroupTreeNode:
        def __init__(self, name: Optional[str] = None):
            self._name = name

            self._children: Dict[str, "VariableCache.GroupTreeNode"] = {}

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, name: Optional[str]):
            self._name = name

        def add_child(self, path_component: str, child: "VariableCache.GroupTreeNode"):
            self._children[path_component] = child

        def is_leaf(self) -> bool:
            return len(self._children) == 0

        def __len__(self):
            return len(self._children)

        def __contains__(self, component: str):
            return component in self._children

        def __getitem__(self, component: str):
            return self._children[component]

        def get(
            self, component, default: Optional["VariableCache.GroupTreeNode"] = None
        ):
            return self._children.get(component, default)

        def leaves(self) -> Generator["VariableCache.GroupTreeNode", None, None]:
            if self.is_leaf():
                yield self
            for child in self._children.values():
                yield from child.leaves()

        def leaf_variables(self) -> Generator[str, None, None]:
            yield from (leaf.name for leaf in self.leaves())

        def _min_leaf_name(self) -> str:
            return min(self.leaf_variables())

        def _node_str(self, level: int, component: str, indent_prefix: str) -> str:
            line = indent_prefix * level
            if len(self._children) > 0 or self._name is not None:
                line = f"{line}+ {component}"
            if self.name is not None:
                line = f"{line} ({self.name})"

            return line

        def _subtree_str(self, level: int, component: str, indent_prefix: str) -> str:
            rep = self._node_str(level, component, indent_prefix)
            for path_component, child in sorted(
                self._children.items(), key=lambda t: t[1]._min_leaf_name()
            ):
                rep = (
                    rep
                    + "\n"
                    + child._subtree_str(level + 1, path_component, indent_prefix)
                )
            return rep

        def __str__(self) -> str:
            return "\n".join(
                child._subtree_str(0, path_component, indent_prefix="    ")
                for path_component, child in sorted(
                    self._children.items(), key=lambda t: t[1]._min_leaf_name()
                )
            )

    def group_tree(
        self, dataset: str, year: int, group_name: str, *, skip_annotations: bool = True
    ) -> "VariableCache.GroupTreeNode":
        group = self.get_group(dataset, year, group_name)

        root = VariableCache.GroupTreeNode()

        for variable_name, details in group.items():
            path = details["label"].split("!!")

            node = root

            # Construct a nested path of nodes down to the
            # leaf.
            for component in path:
                child = node.get(component, None)
                if child is None:
                    child = VariableCache.GroupTreeNode()
                    node.add_child(component, child)
                node = child

            # Put the variable name at the lead.
            node.name = variable_name

        return root

    def group_leaves(
        self, dataset: str, year: int, name: str, *, skip_annotations: bool = True
    ) -> List[str]:
        """
        Find the leaves of a given group.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        name
            The name of the group.
        skip_annotations
            If `True` try to filter out variables that are
            annotations rather than actual values, by skipping
            those with labels that begin with `Annotation` or
            'Margin of Error`.

        Returns
        -------
            A list of the variables in the group that are leaves,
            i.e. they are not aggregates of other variables. For example,
            in the group `B03002` in from the `acs/acs5` source in the
            year `2020`, the variable `B03002_003E` is a leaf, because
            it represents
            `"Estimate!!Total:!!Not Hispanic or Latino:!!White alone"`,
            whereas B03002_002E is not a leaf because it represents
            `"Estimate!!Total:!!Not Hispanic or Latino:", which is a total
            that includes B03002_003E as well as others like `"B03002_004E"`,
            `"B03002_005E" and more.

            The typical reason we want leaves is because that gives us a set
            of variables representing counts that do not overalap and add up
            to the total. We can use these directly in diversity and integration
            calculations using the `divintseg` package.`
        """
        tree = self.group_tree(dataset, year, name)
        leaves = tree.leaf_variables()

        if skip_annotations:
            group = self.get_group(dataset, year, name)
            leaves = (
                leaf
                for leaf in leaves
                if (not group[leaf]["label"].startswith("Annotation"))
                and (not group[leaf]["label"].startswith("Margin of Error"))
            )

        return sorted(leaves)

    def __contains__(self, item: Tuple[str, int, str]) -> bool:
        """Magic method behind the `in` operator."""
        source, year, name = item

        return name in self._variable_cache[source][year]

    def __getitem__(self, item: Tuple[str, int, str]):
        """Magic method behind the `[]` operator."""
        return self.get(*item)

    def __len__(self):
        """The number of elements in the cache."""
        return sum(
            len(names)
            for years in self._variable_cache.values()
            for names in years.values()
        )

    def keys(self) -> Iterable[Tuple[str, int, str]]:
        """Keys, i.e. the names of variables, in the cache."""
        for key, _ in self.items():
            yield key

    def __iter__(self) -> Iterable[Tuple[str, int, str]]:
        return self.keys()

    def values(self) -> Iterable[dict]:
        """Values, i.e. the descriptions of variables, in the cache."""
        for _, value in self.items():
            yield value

    def items(self) -> Iterable[Tuple[Tuple[str, int, str], dict]]:
        """Items in the mapping from variable name to descpription."""
        for source, values_for_source in self._variable_cache.items():
            for year, values_for_year in values_for_source.items():
                for name, value in values_for_year.items():
                    yield (source, year, name), value

    def invalidate(self, dataset: str, year: int, name: str):
        """Remove an item from the cache."""
        if self._variable_cache[dataset][year].pop(name, None):
            if len(self._variable_cache[dataset][year]) == 0:
                self._variable_cache[dataset].pop(year)
                if len(self._variable_cache[dataset]) == 0:
                    self._variable_cache.pop(dataset)

    def clear(self):
        """
        Clear the entire cache.

        This just means that further calls to :py:meth:`~get` will
        have to make a call to the source behind the cache.
        """
        self._variable_cache = defaultdict(lambda: defaultdict(dict))


variables = VariableCache()
