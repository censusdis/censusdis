import itertools
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union, ClassVar

import geopandas as gpd
import pandas as pd
import yaml

import censusdis.data as ced
import censusdis.maps as cem
import censusdis.datasets
from censusdis.geography import InSpecType
from censusdis.impl.varsource.base import VintageType


def _class_constructor(clazz: ClassVar):
    def constructor(
        loader: yaml.SafeLoader, node: yaml.nodes.MappingNode
    ) -> VariableSpec:
        """Construct a new object of the given class."""
        kwargs = loader.construct_mapping(node, deep=True)
        return clazz(**kwargs)

    return constructor


class VariableSpec:
    def __init__(
        self,
        *,
        denominator: Union[str, bool] = False,
        frac_prefix: Optional[str] = None,
    ):
        self._denominator = denominator

        if frac_prefix is None:
            frac_prefix = "frac_"

        self._frac_prefix = frac_prefix

    @property
    def denominator(self) -> Union[str, bool]:
        return self._denominator

    @property
    def frac_prefix(self) -> str:
        return self._frac_prefix

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
            row_keys=row_keys,
            **kwargs,
        )

        self.synthesize(df_or_gdf)

        return df_or_gdf

    @classmethod
    def yaml_loader(cls):
        loader = yaml.SafeLoader
        loader.add_constructor("!VariableList", _class_constructor(VariableList))
        loader.add_constructor("!Group", _class_constructor(CensusGroup))
        loader.add_constructor("!SpecCollection", _variable_spec_collection_constructor)
        return loader

    @classmethod
    def load_yaml(cls, path: Union[str, Path]):
        loader = cls.yaml_loader()

        loaded = yaml.load(open(path, "rb"), Loader=loader)

        return loaded


class VariableList(VariableSpec):
    def __init__(
        self,
        variables: Union[str, Iterable[str]],
        *,
        denominator: Union[str, bool] = False,
        frac_prefix: Optional[str] = None,
    ):
        super().__init__(denominator=denominator, frac_prefix=frac_prefix)
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
                df_downloaded[f"{self.frac_prefix}{variable}"] = (
                    df_downloaded[variable] / df_downloaded[self.denominator]
                )
        elif self.denominator:
            denominator = df_downloaded[self._variables].sum(axis="columns")
            for variable in self._variables:
                df_downloaded[f"{self.frac_prefix}{variable}"] = (
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
        frac_prefix: Optional[str] = None,
    ):
        if denominator is None:
            denominator = False

        super().__init__(denominator=denominator, frac_prefix=frac_prefix)
        self._group = [group] if isinstance(group, str) else list(group)
        self._leaves_only = leaves_only

    def groups_to_download(self) -> List[Tuple[str, bool]]:
        return [(group, self._leaves_only) for group in self._group]

    def synthesize(self, df_downloaded: Union[pd.DataFrame, gpd.GeoDataFrame]):
        if isinstance(self.denominator, str):
            for group in self._group:
                for variable in df_downloaded.columns:
                    if variable.startswith(group):
                        df_downloaded[f"{self.frac_prefix}{variable}"] = (
                            df_downloaded[variable] / df_downloaded[self.denominator]
                        )
        elif self.denominator:
            for group in self._group:
                denominator = df_downloaded[
                    [
                        variable
                        for variable in df_downloaded.columns
                        if variable.startswith(group)
                    ]
                ].sum(axis="columns")
                for variable in df_downloaded.columns:
                    if variable.startswith(group):
                        df_downloaded[f"{self.frac_prefix}{variable}"] = (
                            df_downloaded[variable] / denominator
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


def _variable_spec_collection_constructor(
    loader: yaml.SafeLoader, node: yaml.nodes.SequenceNode
) -> VariableSpecCollection:
    """Construct a variable spec collection."""
    variable_specs = loader.construct_sequence(node, deep=True)
    return VariableSpecCollection(variable_specs)


class DataSpec:
    def __init__(
        self,
        dataset: str,
        vintage: VintageType,
        specs: Union[VariableSpec, Iterable[VariableSpec]],
        geography: Dict[str, str],
        *,
        with_geometry: bool = False,
        remove_water: bool = False,
    ):
        # Map symbolic names or use what we are given if there is no mapping.
        self._dataset = getattr(censusdis.datasets, dataset, dataset)
        self._vintage = vintage
        self._variable_spec = (
            specs if isinstance(specs, VariableSpec) else VariableSpecCollection(specs)
        )
        self._geography = geography
        self._with_geometry = with_geometry
        self._remove_water = remove_water

    @property
    def dataset(self) -> str:
        return self._dataset

    @property
    def vintage(self) -> VintageType:
        return self._vintage

    @property
    def with_geometry(self) -> bool:
        return self._with_geometry

    @property
    def remove_water(self) -> bool:
        return self._remove_water

    @property
    def variable_spec(self) -> VariableSpec:
        return self._variable_spec

    def download(
        self,
        api_key: Optional[str] = None,
    ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        return self._variable_spec.download(
            dataset=self.dataset,
            vintage=self._vintage,
            with_geometry=self._with_geometry,
            remove_water=self._remove_water,
            api_key=api_key,
            **self._geography,
        )

    @classmethod
    def yaml_loader(cls):
        loader = VariableSpec.yaml_loader()
        loader.add_constructor("!DataSpec", _class_constructor(cls))
        return loader

    @classmethod
    def load_yaml(cls, path: Union[str, Path]):
        loader = cls.yaml_loader()

        loaded = yaml.load(open(path, "rb"), Loader=loader)

        return loaded


class PlotSpec:
    def __init__(
        self,
        variable: str,
        *,
        boundary: bool = False,
        with_background: bool = False,
        plot_kwargs: Optional[Dict[str, Any]] = None,
        projection: Optional[str] = None,
    ):
        self._variable = variable
        self._boundary = boundary
        self._with_background = with_background
        if plot_kwargs is None:
            plot_kwargs: Dict[str, Any] = {}
        self._plot_kwargs = plot_kwargs
        self._projection = projection

    @property
    def variable(self) -> str:
        return self._variable

    @property
    def boundary(self) -> bool:
        return self._boundary

    @property
    def with_background(self) -> bool:
        return self._with_background

    @property
    def plot_kwargs(self) -> Dict[str, Any]:
        return self._plot_kwargs

    @property
    def projection(self):
        return self._projection

    def __eq__(self, other) -> bool:
        if not isinstance(other, PlotSpec):
            return False

        return (
            self._variable == other._variable
            and self._boundary == other._boundary
            and self._with_background == other._with_background
            and self._projection == other._projection
            and self._plot_kwargs == other._plot_kwargs
        )

    def plot(self, gdf: gpd.GeoDataFrame):
        if self._projection in ["US", "us", "U.S."]:
            if self._boundary:
                ax = cem.plot_us_boundary(
                    gdf,
                    self._variable,
                    with_background=self._with_background,
                    do_relocate_ak_hi_pr=True,
                    **self._plot_kwargs,
                )
            else:
                ax = cem.plot_us(
                    gdf,
                    self._variable,
                    with_background=self._with_background,
                    do_relocate_ak_hi_pr=True,
                    **self._plot_kwargs,
                )
        else:
            if self._projection is not None:
                gdf = gdf.to_crs(epsg=self._projection)

            if self._boundary:
                gdf = gdf.boundary

            ax = cem.plot_map(
                gdf,
                self._variable,
                with_background=self._with_background,
                **self.plot_kwargs,
            )

        return ax

    @classmethod
    def yaml_loader(cls):
        loader = yaml.SafeLoader
        loader.add_constructor("!PlotSpec", _class_constructor(cls))
        return loader

    @classmethod
    def load_yaml(cls, path: Union[str, Path]) -> "PlotSpec":
        loader = cls.yaml_loader()

        loaded = yaml.load(open(path, "rb"), Loader=loader)

        return loaded
