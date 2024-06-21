# Copyright (c) 2022 Darren Erik Vengroff
"""Variable cache code to cache metatada about variables locally."""

from collections import defaultdict
from logging import getLogger
from typing import (
    Any,
    DefaultDict,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

import numpy as np
import pandas as pd

from censusdis import CensusApiException
from censusdis.impl.varsource.base import VariableSource
from censusdis.impl.varsource.censusapi import CensusApiVariableSource

import censusdis.datasets

import re


logger = getLogger(__name__)


class VariableCache:
    """
    A cache of variables and groups.

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
        self._variable_cache: DefaultDict[str, DefaultDict[int, Dict[str, Any]]] = (
            defaultdict(lambda: defaultdict(dict))
        )
        self._group_cache: DefaultDict[str, DefaultDict[int, Dict[str, Any]]] = (
            defaultdict(lambda: defaultdict(dict))
        )

        self._all_data_sets_cache: Optional[pd.DataFrame] = None
        self._data_sets_by_year_cache: Dict[int, pd.DataFrame] = {}

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
        name: Optional[str],
        skip_subgroup_variables: bool = True,
    ) -> Dict[str, Dict]:
        """
        Get information on the variables in a group.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        name
            The name of the group. Or None if this data set does not have
            groups.
        skip_subgroup_variables
            If this is `True`, then we will ignore variables from alphabetical
            subgroups. These are relatively common in the ACS, where there are
            groups like `B01001` that have subgroups `B01001A`, `B01001B` and
            so on. The underlying census API sometimes reports variables like
            `B01001A_001E` from these as members of `B01001` and other times as
            members of `B01001A`. Setting this `True`, which is the default,
            does not report `B01001A_001E` when the group name `name='B01001'`.

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

        # Optionally filter out the variables that are in
        # alphabetical subgroups.
        if skip_subgroup_variables and name is not None:
            subgroup_var_pattern = re.compile(f"^{name}[A-Z]_.*$")
            group_variable_names = [
                group_variable_name
                for group_variable_name in group_variable_names
                if not (
                    group_variable_name.startswith(name)
                    and subgroup_var_pattern.match(group_variable_name)
                )
            ]

        # Reformat what we return so it includes the full
        # details on each variable.
        return {
            group_variable_name: self.get(dataset, year, group_variable_name)
            for group_variable_name in group_variable_names
        }

    class GroupTreeNode:
        """A node in a tree of variables that make up a group."""

        def __init__(self, name: Optional[str] = None):
            self._name = name

            self._children: Dict[str, "VariableCache.GroupTreeNode"] = {}

        @property
        def name(self):
            """The name of the node."""
            return self._name

        @name.setter
        def name(self, name: Optional[str]):
            self._name = name

        def add_child(self, path_component: str, child: "VariableCache.GroupTreeNode"):
            """
            Add a child to a node.

            Parameters
            ----------
            path_component
                The next component of the path to the variable, beyond the
                path to `self`.
            child
                The node that should be our child at the specified path component.

            Returns
            -------
                None
            """
            self._children[path_component] = child

        def is_leaf(self) -> bool:
            """
            Is the node a leaf.

            Returns
            -------
                `True` if it is a leaf; `False` if it is an internal node.
            """
            return len(self._children) == 0

        def __len__(self):
            """Return the number of children the node has."""
            return len(self._children)

        def __contains__(self, component: str):
            """Determine if a component is in the node."""
            return component in self._children

        def __getitem__(self, component: str):
            """Get a child of a node."""
            return self._children[component]

        def keys(self) -> Generator[str, None, None]:
            """
            Return the keys, which are the strings of the next component to each child.

            Returns
            -------
                The keys
            """
            for key, _ in self.items():
                yield key

        def values(self) -> Generator["VariableCache.GroupTreeNode", None, None]:
            """
            Return the values, which are our children.

            Returns
            -------
                The values (our children).
            """
            for _, value in self.items():
                yield value

        def items(
            self,
        ) -> Generator[Tuple[str, "VariableCache.GroupTreeNode"], None, None]:
            """
            Retudn the items.

            The items are (key, value) pairs. See :py:meth:`keys` and
            :py:meth:`values`.

            Returns
            -------
                The items
            """
            for component, node in self._children.items():
                yield component, node

        def get(
            self, component, default: Optional["VariableCache.GroupTreeNode"] = None
        ):
            """
            Get the child at the given path component below us.

            Parameters
            ----------
            component
                The next component of the path below us.
            default
                The default value to return if there is no node at the path.

            Returns
            -------
                The node below us or `default` if it is not there,
            """
            return self._children.get(component, default)

        def leaves(self) -> Generator["VariableCache.GroupTreeNode", None, None]:
            """
            Return all the leaves below us.

            Compare with :py:meth:`~leaf_variables`
            which returns just the names of the leaves.

            Returns
            -------
                All the leaves below us.
            """
            if self.is_leaf():
                yield self
            for child in self._children.values():
                yield from child.leaves()

        def leaf_variables(self) -> Generator[str, None, None]:
            """
            Return the names of all the leaves below us.

            Compare with :py:meth:`~leaves`
            which returns the full node for each leaf.

            Returns
            -------
                The names of the leaves below us.
            """
            yield from (leaf.name for leaf in self.leaves())

        @property
        def min_leaf_name(self) -> str:
            """The name of the first leaf."""
            return min(self.leaf_variables())

        def _node_str(self, level: int, component: str, indent_prefix: str) -> str:
            line = indent_prefix * level
            if len(self._children) > 0 or self._name is not None:
                line = f"{line}+ {component}"
            if self.name is not None:
                line = f"{line} ({self.name})"

            return line

        def subtree_str(self, level: int, component: str, indent_prefix: str) -> str:
            """
            Return a string representing a subtree.

            Used to construct an indented string representation for the whole tree.
            """
            rep = self._node_str(level, component, indent_prefix)
            for path_component, child in sorted(
                self._children.items(), key=lambda t: t[1].min_leaf_name
            ):
                rep = (
                    rep
                    + "\n"
                    + child.subtree_str(level + 1, path_component, indent_prefix)
                )
            return rep

        def __str__(self) -> str:
            """Return a string representation of the node."""
            return "\n".join(
                child.subtree_str(0, path_component, indent_prefix="    ")
                for path_component, child in sorted(
                    self._children.items(), key=lambda t: t[1].min_leaf_name
                )
            )

        def __repr__(self) -> str:
            """Return the representation of the node."""
            return str(self)

    def _all_data_sets(self) -> pd.DataFrame:
        """
        Get all the data sets.

        Cache to avoid repeated remote calls.

        Returns
        -------
            A data frame of all the data sets for all years.
        """
        if self._all_data_sets_cache is None:
            datasets = self._variable_source.get_datasets(year=None)

            self._all_data_sets_cache = self._datasets_from_source_dict(datasets)

        return self._all_data_sets_cache

    def _data_sets_for_year(self, year: int) -> pd.DataFrame:
        """
        Get all data sets for a given year.

        Cache to avoid repeated remote calls.

        Parameters
        ----------
        year
            The year to query. If not provided, all data sets for all
            years are queried.

        Returns
        -------
            A data frame of all the data sets for the year.
        """
        if year not in self._data_sets_by_year_cache:
            datasets = self._variable_source.get_datasets(year)

            self._data_sets_by_year_cache[year] = self._datasets_from_source_dict(
                datasets
            )

        return self._data_sets_by_year_cache[year]

    @staticmethod
    def _datasets_from_source_dict(datasets) -> pd.DataFrame:
        """
        Parse a dict from :py:meth:`VariableSource.get_datasets` into a data frame of data sets.

        Parameters
        ----------
        datasets
            The data sets in dictionary form.

        Returns
        -------
            A dataframe with a row describing each dataset.
        """
        datasets = datasets["dataset"]
        df_datasets = pd.DataFrame(
            [
                {
                    "YEAR": dataset.get(
                        "c_vintage",
                        "timeseries" if dataset.get("c_isTimeseries", False) else None,
                    ),
                    "DATASET": "/".join(dataset["c_dataset"]),
                    "TITLE": dataset.get("title", None),
                    "DESCRIPTION": dataset.get("description", None),
                    "API BASE URL": (
                        dataset["distribution"][0].get("accessURL", None)
                        if dataset.get("distribution")
                        else None
                    ),
                }
                for dataset in datasets
            ]
        )

        symbol_dict_reversed = {
            value: symbol
            for symbol, value in censusdis.datasets.__dict__.items()
            if isinstance(value, str)
        }

        df_datasets["SYMBOL"] = df_datasets["DATASET"].apply(
            lambda name: symbol_dict_reversed.get(name, None)
        )

        df_datasets = df_datasets[
            ["YEAR", "SYMBOL", "DATASET"]
            + [
                col
                for col in df_datasets.columns
                if col not in ["YEAR", "SYMBOL", "DATASET"]
            ]
        ]

        return df_datasets.sort_values(["YEAR", "DATASET"]).reset_index(drop=True)

    def all_data_sets(self, *, year: Optional[int] = None) -> pd.DataFrame:
        """
        Retrieve a description of available data sets.

        Parameters
        ----------
        year
            The year to query. If not provided, all data sets for all
            years are queried.

        Returns
        -------
            A data frame describing the data sets that are available.
        """
        if year is not None:
            return self._data_sets_for_year(year)

        return self._all_data_sets()

    @staticmethod
    def _compile_pattern(pattern, case):
        """Compile patterns passed to search methods with case flag."""
        if isinstance(pattern, str):
            flags = re.IGNORECASE if not case else 0
            pattern = re.compile(pattern, flags=flags)
        return pattern

    def search_data_sets(
        self,
        *,
        vintage: Optional[Union[int, Iterable[int]]] = None,
        pattern: Optional[Union[str, re.Pattern]] = None,
        case: bool = False,
    ) -> pd.DataFrame:
        """
        Search for data sets over one or more vintages.

        Parameters
        ----------
        vintage
            One or more Vintages to explore.
        pattern
            A regular expression to match against the name and description of a variable. This
            is used to filter down results. Normally at most one of `name` and `re` will be used.
        case:
            If `patters` is not `None` then indicates whether the regular expression match is
            case sensitive. Does not affect the `name` match.

        Returns
        -------
            A data frame of matching variables.
        """
        if vintage is None or isinstance(vintage, int):
            vintage = [vintage]

        df_datasets = pd.concat(
            (self.all_data_sets(year=year) for year in vintage), ignore_index=True
        )

        if pattern is not None:
            pattern = self._compile_pattern(pattern, case)

            df_matches = df_datasets[
                df_datasets["SYMBOL"].str.contains(pattern)
                | df_datasets["DATASET"].str.contains(pattern)
                | df_datasets["TITLE"].str.contains(pattern)
                | df_datasets["DESCRIPTION"].str.contains(pattern)
            ]
        else:
            df_matches = df_datasets

        return df_matches.reset_index(drop=True)

    def all_groups(
        self,
        dataset: str,
        year: int,
    ) -> pd.DataFrame:
        """
        Get descriptions of all the groups in the data set.

        Parameters
        ----------
        dataset
            The data set.
        year
            The year.

        Returns
        -------
            Metadata on all the groups in the data set.
        """
        groups = self._variable_source.get_all_groups(dataset, year)

        # Some data sets have no groups.
        if len(groups["groups"]) == 0:
            return pd.DataFrame(columns=["DATASET", "YEAR", "GROUP", "DESCRIPTION"])

        return (
            pd.DataFrame(
                [
                    {
                        "DATASET": dataset,
                        "YEAR": year,
                        "GROUP": group["name"],
                        "DESCRIPTION": group["description"],
                    }
                    for group in groups["groups"]
                ]
            )
            .sort_values(["DATASET", "YEAR", "GROUP"])
            .reset_index(drop=True)
        )

    def search_groups(
        self,
        dataset: str,
        vintage: Union[int, Iterable[int]],
        *,
        pattern: Optional[Union[str, re.Pattern]] = None,
        case: bool = False,
    ) -> pd.DataFrame:
        """
        Search for groups in a data set over one or more vintages.

        Parameters
        ----------
        dataset
            The data set.
        vintage
            One or more Vintages to explore.
        pattern
            A regular expression to match against the name and description of a variable. This
            is used to filter down results. Normally at most one of `name` and `re` will be used.
        case:
            If `patters` is not `None` then indicates whether the regular expression match is
            case sensitive. Does not affect the `name` match.

        Returns
        -------
            A data frame of matching variables.
        """
        if vintage is None or isinstance(vintage, int):
            vintage = [vintage]

        def _all_groups_eat_404(year: int):
            """
            Skip bad year and return no results.

            We assume it is a bad year if we get a 404.
            """
            try:
                return self.all_groups(dataset, year)
            except CensusApiException as e:
                if "404" in str(e):
                    return pd.DataFrame()
                else:
                    raise e

        df_groups = pd.concat(
            (_all_groups_eat_404(year) for year in vintage), ignore_index=True
        )

        if pattern is not None:
            pattern = self._compile_pattern(pattern, case)

            df_matches = df_groups[
                df_groups["GROUP"].str.contains(pattern)
                | df_groups["DESCRIPTION"].str.contains(pattern)
            ]
        else:
            df_matches = df_groups

        return df_matches.reset_index(drop=True)

    def all_variables(
        self,
        dataset: str,
        year: int,
        group_name: Optional[str],
        *,
        skip_annotations: bool = True,
        skip_subgroup_variables: bool = True,
    ) -> pd.DataFrame:
        """
        Produce a data frame of metadata on all variables in a group.

        Parameters
        ----------
        dataset
            The data set.
        year
            The year.
        group_name
            The group.
        skip_annotations
            If `True` try to filter out variables that are
            annotations rather than actual values, by skipping
            those with labels that begin with "Annotation" or
            "Margin of Error".
        skip_subgroup_variables
            If this is `True`, then we will ignore variables from alphabetical
            subgroups. These are relatively common in the ACS, where there are
            groups like `B01001` that have subgroups `B01001A`, `B01001B` and
            so on. The underlying census API sometimes reports variables like
            `B01001A_001E` from these as members of `B01001` and other times as
            members of `B01001A`. Setting this `True`, which is the default,
            does not report `B01001A_001E` when the group name `name='B01001'`.

        Returns
        -------
            Metadata on all variables in the group.
        """
        group_variables = self.group_variables(
            dataset,
            year,
            group_name,
            skip_annotations=skip_annotations,
            skip_subgroup_variables=skip_subgroup_variables,
        )

        def variable_items(variable_dict: Dict) -> Optional[Dict[str, str]]:
            if "values" in variable_dict:
                values = variable_dict["values"]
                return values.get("item", np.nan)

            return None

        return pd.DataFrame(
            [
                {
                    "YEAR": year,
                    "DATASET": dataset,
                    "GROUP": self.get(dataset, year, variable_name).get(
                        "group", np.nan
                    ),
                    "VARIABLE": variable_name,
                    "LABEL": self.get(dataset, year, variable_name)["label"],
                    "SUGGESTED_WEIGHT": self.get(dataset, year, variable_name).get(
                        "suggested-weight", np.nan
                    ),
                    "VALUES": variable_items(self.get(dataset, year, variable_name)),
                }
                for variable_name in group_variables
            ]
        )

    def search(
        self,
        dataset: str,
        vintage: Union[int, Iterable[int]],
        *,
        group_name: Optional[str] = None,
        name: Optional[Union[str, Iterable[str]]] = None,
        pattern: Optional[Union[str, re.Pattern]] = None,
        case: bool = False,
        skip_annotations: bool = True,
        skip_subgroup_variables: bool = True,
    ) -> pd.DataFrame:
        """
        Search for variables in a data set over one or more vintages.

        Parameters
        ----------
        dataset
            The data set.
        vintage
            One or more Vintages to explore.
        group_name
            The group if we should explore only a single group. If `None` all groups
            will be explored.
        name
            The name of one of more variables to explore. If `None` all variables are considered.
            Normally at most one of `name` and `re` will be used.
        pattern
            A regular expression to match against the name and description of a variable. This
            is used to filter down results. Normally at most one of `name` and `re` will be used.
        case:
            If `patters` is not `None` then indicates whether the regular expression match is
            case sensitive. Does not affect the `name` match.
        skip_annotations
            If `True` try to filter out variables that are
            annotations rather than actual values, by skipping
            those with labels that begin with "Annotation" or
            "Margin of Error".
        skip_subgroup_variables
            If this is `True`, then we will ignore variables from alphabetical
            subgroups. These are relatively common in the ACS, where there are
            groups like `B01001` that have subgroups `B01001A`, `B01001B` and
            so on. The underlying census API sometimes reports variables like
            `B01001A_001E` from these as members of `B01001` and other times as
            members of `B01001A`. Setting this `True`, which is the default,
            does not report `B01001A_001E` when the group name `name='B01001'`.

        Returns
        -------
            A data frame of matching variables.
        """
        if isinstance(vintage, int):
            vintage = [vintage]

        def _all_variables_eat_404(year: int):
            """
            Skip bad year and return no results.

            We assume it is a bad year if we get a 404.
            """
            try:
                return self.all_variables(
                    dataset,
                    year,
                    group_name,
                    skip_annotations=skip_annotations,
                    skip_subgroup_variables=skip_subgroup_variables,
                )
            except CensusApiException as e:
                if "404" in str(e):
                    return pd.DataFrame()
                else:
                    raise e

        df_all_variables = pd.concat(
            (_all_variables_eat_404(year) for year in vintage), ignore_index=True
        )

        # If we were given names to match on, then match on them.
        if name is not None:
            if isinstance(name, str):
                name = [name]

            df_name_matches = pd.concat(
                [
                    df_all_variables[df_all_variables["VARIABLE"] == var_name]
                    for var_name in name
                ],
                axis="rows",
            )
        else:
            df_name_matches = df_all_variables

        if pattern is not None:
            pattern = self._compile_pattern(pattern, case)

            df_matches = df_name_matches[
                (
                    df_name_matches["VARIABLE"].str.contains(pattern)
                    | df_name_matches["LABEL"].str.contains(pattern)
                )
            ]
        else:
            df_matches = df_name_matches

        return pd.DataFrame(df_matches).reset_index(drop=True)

    def group_tree(
        self,
        dataset: str,
        year: int,
        group_name: Optional[str],
        *,
        skip_annotations: bool = True,
    ) -> "VariableCache.GroupTreeNode":
        """
        Construct a tree that embodies the parent/child relationships of all the variables in a group.

        Parameters
        ----------
        dataset
            The data set.
        year
            The year.
        group_name
            The group.
        skip_annotations
            If `True`, skip variables that are annotations of others, like
            margin of error.

        Returns
        -------
            A tree that can be printed or walked.
        """
        group = self.get_group(dataset, year, group_name)

        root = VariableCache.GroupTreeNode()

        for variable_name, details in group.items():
            path = details["label"].split("!!")

            if skip_annotations and (
                path[0].startswith("Annotation")
                or path[0].startswith("Margin of Error")
                or path[0].startswith("Statistical Significance")
            ):
                continue

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
            those with labels that begin with "Annotation" or
            "Margin of Error".

        Returns
        -------
            A list of the variables in the group that are leaves,
            i.e. they are not aggregates of other variables. For example,
            in the group `B03002` in the `acs/acs5` dataset in the
            year `2020`, the variable `B03002_003E` is a leaf, because
            it represents
            "Estimate!!Total:!!Not Hispanic or Latino:!!White alone",
            whereas B03002_002E is not a leaf because it represents
            "Estimate!!Total:!!Not Hispanic or Latino:", which is a total
            that includes B03002_003E as well as others like "B03002_004E",
            "B03002_005E" and more.

            The typical reason we want leaves is because that gives us a set
            of variables representing counts that do not overlap and add up
            to the total. We can use these directly in diversity and integration
            calculations using the `divintseg` package.
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

    def group_variables(
        self,
        dataset: str,
        year: int,
        group_name: str,
        *,
        skip_annotations: bool = True,
        skip_subgroup_variables: bool = True,
    ) -> List[str]:
        """
        Find the variables of a given group.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        group_name
            The name of the group.
        skip_annotations
            If `True` try to filter out variables that are
            annotations rather than actual values, by skipping
            those with labels that begin with "Annotation" or
            "Margin of Error".
        skip_subgroup_variables
            If this is `True`, then we will ignore variables from alphabetical
            subgroups. These are relatively common in the ACS, where there are
            groups like `B01001` that have subgroups `B01001A`, `B01001B` and
            so on. The underlying census API sometimes reports variables like
            `B01001A_001E` from these as members of `B01001` and other times as
            members of `B01001A`. Setting this `True`, which is the default,
            does not report `B01001A_001E` when the group name `name='B01001'`.

        Returns
        -------
            A list of the variables in the group.
        """
        tree = self.get_group(
            dataset, year, group_name, skip_subgroup_variables=skip_subgroup_variables
        )

        if skip_annotations:
            group_variables = [
                k
                for k, v in tree.items()
                if (not v["label"].startswith("Annotation"))
                and (not v["label"].startswith("Margin of Error"))
            ]
        else:
            group_variables = list(tree.keys())

        return sorted(group_variables)

    def __contains__(self, item: Tuple[str, int, str]) -> bool:
        """Magic method behind the `in` operator."""
        source, year, name = item

        return name in self._variable_cache[source][year]

    def __getitem__(self, item: Tuple[str, int, str]):
        """Magic method behind the `[]` operator."""
        return self.get(*item)

    def __len__(self):
        """Return he number of elements in the cache."""
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
        """Return an iterator over the keys."""
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
