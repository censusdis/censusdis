# Copyright (c) 2022 Darren Erik Vengroff
"""
Variable cache code to cache metatada about variables locally.
"""

from collections import defaultdict
from typing import Any, DefaultDict, Dict, Generator, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

from censusdis.impl.varsource.base import VariableSource
from censusdis.impl.varsource.censusapi import CensusApiVariableSource


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
        self._variable_cache: DefaultDict[
            str, DefaultDict[int, Dict[str, Any]]
        ] = defaultdict(lambda: defaultdict(dict))
        self._group_cache: DefaultDict[
            str, DefaultDict[int, Dict[str, Any]]
        ] = defaultdict(lambda: defaultdict(dict))

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

        def keys(self) -> Iterable[str]:
            for key, _ in self.items():
                yield key

        def values(self) -> Iterable["VariableCache.GroupTreeNode"]:
            for _, value in self.items():
                yield value

        def items(self) -> Iterable[Tuple[str, "VariableCache.GroupTreeNode"]]:
            return self._children.items()

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

        def __repr__(self) -> str:
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
        df = pd.DataFrame(
            [
                {
                    "YEAR": dataset.get("c_vintage", None),
                    "DATASET": "/".join(dataset["c_dataset"]),
                    "TITLE": dataset.get("title", None),
                    "DESCRIPTION": dataset.get("description", None),
                }
                for dataset in datasets
            ]
        )
        return df.sort_values(["YEAR", "DATASET"]).reset_index(drop=True)

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
            All the groups in the data set.
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

    def all_variables(
        self, dataset: str, year: int, group_name: Optional[str]
    ) -> pd.DataFrame:
        group_variables = self.group_variables(dataset, year, group_name)

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

    def group_tree(
        self,
        dataset: str,
        year: int,
        group_name: Optional[str],
        *,
        skip_annotations: bool = True,
    ) -> "VariableCache.GroupTreeNode":
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
        self, dataset: str, year: int, group_name: str, *, skip_annotations: bool = True
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

        Returns
        -------
            A list of the variables in the group.
        """
        tree = self.get_group(dataset, year, group_name)

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
