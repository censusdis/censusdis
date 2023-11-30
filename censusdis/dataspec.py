from typing import ClassVar, List, Iterable, Optional, Tuple, Union
import itertools
import pandas as pd
import geopandas as gpd
import yaml
from pathlib import Path
import censusdis.data as ced
from censusdis.geography import InSpecType
from censusdis.impl.varsource.base import VintageType


class VariableSpec:
    def __init__(self, *, denominator: Union[str, bool] = False):
        self._denominator = denominator

    @property
    def denominator(self) -> Union[str, bool]:
        return self._denominator

    def variables_to_download(self) -> List[str]:
        if isinstance(self._denominator, str):
            return [self._denominator]

        return []

    def groups_to_download(self) -> List[Tuple[str, bool]]:
        return []

    def synthesize(self, df_downloaded: Union[pd.DataFrame, gpd.GeoDataFrame]):
        return df_downloaded

    def download(
        self,
        dataset: str,
        vintage: VintageType,
        *,
        set_to_nan: Union[bool, Iterable[int]] = True,
        skip_annotations: bool = True,
        with_geometry: bool = False,
        remove_water: bool = False,
        api_key: Optional[str] = None,
        variable_cache: Optional[ced.VariableCache] = None,
        row_keys: Optional[Union[str, Iterable[str]]] = None,
        **kwargs: InSpecType,
    ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        group_list = self.groups_to_download()

        groups = [group for group, leaves_only in group_list if not leaves_only]
        leaves_of_groups = [group for group, leaves_only in group_list if leaves_only]

        if len(groups) == 0:
            groups = None

        if len(leaves_of_groups) == 0:
            leaves_of_groups = None

        df_or_gdf = ced.download(
            dataset=dataset,
            vintage=vintage,
            download_variables=self.variables_to_download(),
            group=groups,
            leaves_of_group=leaves_of_groups,
            set_to_nan=set_to_nan,
            skip_annotations=skip_annotations,
            with_geometry=with_geometry,
            remove_water=remove_water,
            api_key=api_key,
            variable_cache=variable_cache,
            row_keys=row_keys,
            **kwargs,
        )

        self.synthesize(df_or_gdf)

        return df_or_gdf

    @classmethod
    def load_yaml(cls, path: Union[str, Path]):
        loader = yaml.SafeLoader
        loader.add_constructor("!VariableList", _class_constructor(VariableList))
        loader.add_constructor("!Group", _class_constructor(CensusGroup))
        loader.add_constructor("!SpecCollection", _variable_spec_collection_constructor)

        loaded = yaml.load(open(path, "rb"), Loader=loader)

        return loaded


class VariableList(VariableSpec):
    def __init__(
        self,
        variables: Union[str, Iterable[str]],
        *,
        denominator: Union[str, bool] = False,
    ):
        super().__init__(denominator=denominator)
        if isinstance(variables, str):
            self._variables = [variables]
        else:
            self._variables = list(variables)

    def variables_to_download(self) -> List[str]:
        if (
            isinstance(self.denominator, str)
            and self.denominator not in self._variables
        ):
            # We specified a specific denominator that was not already
            # one of the variables, so get it.
            return self._variables + [self.denominator]
        else:
            # We don't need to fetch an extra variable for the denominator.
            return self._variables

    def synthesize(self, df_downloaded: Union[pd.DataFrame, gpd.GeoDataFrame]):
        if not self.denominator:
            return df_downloaded

        if isinstance(self.denominator, str):
            for variable in self._variables:
                df_downloaded[f"frac_{variable}"] = (
                    df_downloaded[variable] / df_downloaded[self.denominator]
                )
        elif self.denominator:
            denominator = df_downloaded[self._variables].sum(axis="columns")
            for variable in self._variables:
                df_downloaded[f"frac_{variable}"] = (
                    df_downloaded[variable] / denominator
                )

    def __eq__(self, other) -> bool:
        if not isinstance(other, VariableList):
            return False

        return (
            sorted(self._variables) == sorted(other._variables)
            and self.denominator == other.denominator
        )


class CensusGroup(VariableSpec):
    def __init__(
        self,
        group: Union[str, Iterable[str]],
        *,
        leaves_only: bool = False,
        denominator: Optional[str] = None,
    ):
        if denominator is None:
            denominator = False

        super().__init__(denominator=denominator)
        self._group = [group] if isinstance(group, str) else list(group)
        self._leaves_only = leaves_only

    def groups_to_download(self) -> List[Tuple[str, bool]]:
        return [(group, self._leaves_only) for group in self._group]

    def synthesize(self, df_downloaded: Union[pd.DataFrame, gpd.GeoDataFrame]):
        if isinstance(self.denominator, str):
            for group in self._group:
                for variable in df_downloaded.columns:
                    if variable.startswith(group):
                        df_downloaded[f"frac_{variable}"] = (
                            df_downloaded[variable] / df_downloaded[self.denominator]
                        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, CensusGroup):
            return False

        return (
            sorted(self._group) == sorted(other._group)
            and self.denominator == other.denominator
            and self._leaves_only == other._leaves_only
        )


class VariableSpecCollection(VariableSpec):
    def __init__(self, variable_specs: Iterable[VariableSpec]):
        super().__init__(denominator=None)
        self._variable_specs = list(variable_specs)

    def variables_to_download(self) -> List[str]:
        return list(
            set(
                itertools.chain(
                    *[spec.variables_to_download() for spec in self._variable_specs]
                )
            )
        )

    def groups_to_download(self) -> List[Tuple[str, bool]]:
        return list(
            set(
                itertools.chain(
                    *[spec.groups_to_download() for spec in self._variable_specs]
                )
            )
        )

    def synthesize(self, df_downloaded: Union[pd.DataFrame, gpd.GeoDataFrame]):
        df = df_downloaded
        for spec in self._variable_specs:
            spec.synthesize(df)

    def __eq__(self, other) -> bool:
        if not isinstance(other, VariableSpecCollection):
            return False

        if len(self._variable_specs) != len(other._variable_specs):
            return False

        matched = set()

        # Does every spec in self have a unique match in other?
        for self_spec in self._variable_specs:
            match = False
            # We use ii to record those in other that have been
            # matched so we don't try to match again.
            for ii, other_spec in enumerate(self._variable_specs):
                if ii not in matched and self_spec == other_spec:
                    match = True
                    matched.add(ii)
                    break
            if not match:
                return False

        return True


def _class_constructor(clazz: ClassVar):
    def constructor(
        loader: yaml.SafeLoader, node: yaml.nodes.MappingNode
    ) -> VariableSpec:
        """Construct a new object of the given class."""
        kwargs = loader.construct_mapping(node, deep=True)
        return clazz(**kwargs)

    return constructor


def _variable_spec_collection_constructor(
        loader: yaml.SafeLoader, node: yaml.nodes.SequenceNode
) -> VariableSpecCollection:
    """Construct a variable spec collection."""
    variable_specs = loader.construct_sequence(node, deep=True)
    return VariableSpecCollection(variable_specs)


class DataSpec:
    pass
