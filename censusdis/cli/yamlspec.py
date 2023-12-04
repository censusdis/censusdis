"""Classes that are loaded from YAML config files for the CLI."""
from abc import ABC
import itertools
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union, ClassVar

import geopandas as gpd
import pandas as pd
import yaml

import censusdis.data as ced
import censusdis.maps as cem
import censusdis.datasets
import censusdis.states
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


class VariableSpec(ABC):
    """Abstract ase class for specification of variables to download from the U.S. Census API."""

    def __init__(
        self,
        *,
        denominator: Union[str, bool] = False,
        frac_prefix: Optional[str] = None,
    ):
        """
        Specification of variables to download from the U.S. Census API.

        Parameters
        ----------
        denominator
            The denominator to divide by when constructing fractional variables.
            If `False` then no fractional variables are added. If the name of a
            variable, that variable will be downloaded and used as a denominator
            to compute fractional versions of all of the other variables. If `True`
            then the denominator will be computed as the sum of all the other
            variables.
        frac_prefix
            The prefix to prepend to fractional variables. If `None` a default
            prefix of `'frac_'` is used.
        """
        self._denominator = denominator

        if frac_prefix is None:
            frac_prefix = "frac_"

        self._frac_prefix = frac_prefix

    @property
    def denominator(self) -> Union[str, bool]:
        """The denominator to divide by when constructing fractional variables."""
        return self._denominator

    @property
    def frac_prefix(self) -> str:
        """The prefix to prepend to fractional variables."""
        return self._frac_prefix

    def variables_to_download(self) -> List[str]:
        """Return a list of the variables that need to be downloaded from the U.S. Census API."""
        if isinstance(self._denominator, str):
            return [self._denominator]

        return []

    def groups_to_download(self) -> List[Tuple[str, bool]]:
        """
        Return the names of groups of variables that need to be downloaded from the U.S. Census API.

        Returns
        -------
            The names of groups to download.
        """
        return []

    def synthesize(self, df_downloaded: Union[pd.DataFrame, gpd.GeoDataFrame]) -> None:
        """
        Post-process after downloading to compute variables like fractional variables are constructed.

        Parameters
        ----------
        df_downloaded
            A data frame of variables that were downloaded. Any systhesized variables
            are added as new columns.

        Returns
        -------
            None. Any additions are made in-place in `df_downloaded`.
        """
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
        """
        Download the variables we need from the U.S. Census API.

        Most of the optional parameters here mirror those in
        :py:func:`~ced.download`.

        Parameters
        ----------
        dataset
            The dataset to download from. For example `"acs/acs5"`,
            `"dec/pl"`, or `"timeseries/poverty/saipe/schdist"`. There are
            symbolic names for datasets, like `ACS5` for `"acs/acs5"
            in :py:module:`censusdis.datasets`.
        vintage
            The vintage to download data for. For most data sets this is
            an integer year, for example, `2020`. But for
            a timeseries data set, pass the string `'timeseries'`.
        set_to_nan
            A list of values that should be set to NaN. Normally these are special
            values that the U.S. Census API sometimes returns. If `True`, then all
            values in :py:ref:`censusdis.values.ALL_SPECIAL_VALUES` will be replaced.
            If `False`, no replacements will be made.
        skip_annotations
            If `True` try to filter out `group` or `leaves_of_group` variables that are
            annotations rather than actual values. See :py:meth:`VariableCache.group_variables`
            for more details. Variable names passed in `download_variables` are not
            affected by this flag.
        with_geometry
            If `True` a :py:class:`gpd.GeoDataFrame` will be returned and each row
            will have a geometry that is a cartographic boundary suitable for platting
            a map. See https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
            for details of the shapefiles that will be downloaded on your behalf to
            generate these boundaries.
        remove_water
            If `True` and if with_geometry=True, will query TIGER for AREAWATER shapefiles and
            remove water areas from returned geometry.
        api_key
            An optional API key. If you don't have or don't use a key, the number
            of calls you can make will be limited to 500 per day.
        row_keys
            An optional set of identifier keys to help merge together requests for more than the census API limit of
            50 variables per query. These keys are useful for census datasets such as the Current Population Survey
            where the geographic identifiers do not uniquely identify each row.
        kwargs
            A specification of the geometry that we want data for. For example,
            `state = "*", county = "*"` will download county-level data for
            the entire US.

        Returns
        -------
            A :py:class:`~pd.DataFrame` or `~gpd.GeoDataFrame` containing the requested US Census data.
        """
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
    def _yaml_loader(cls):
        loader = yaml.SafeLoader
        loader.add_constructor("!VariableList", _class_constructor(VariableList))
        loader.add_constructor("!Group", _class_constructor(CensusGroup))
        loader.add_constructor("!SpecCollection", _variable_spec_collection_constructor)
        return loader

    @classmethod
    def load_yaml(cls, path: Union[str, Path]):
        """Load a YAML file containing a `VariableSpec`."""
        loader = cls._yaml_loader()

        loaded = yaml.load(open(path, "rb"), Loader=loader)

        return loaded


class VariableList(VariableSpec):
    """Specification of a list of variables to download from the U.S. Census API."""

    def __init__(
        self,
        variables: Union[str, Iterable[str]],
        *,
        denominator: Union[str, bool] = False,
        frac_prefix: Optional[str] = None,
    ):
        """
        Specification of a list of variables to download from the U.S. Census API.

        Parameters
        ----------
        variables
            The variables to download.
        denominator
            The denominator to divide by when constructing fractional variables.
            If `False` then no fractional variables are added. If the name of a
            variable, that variable will be downloaded and used as a denominator
            to compute fractional versions of all of the other variables. If `True`
            then the denominator will be computed as the sum of all the other
            variables.
        frac_prefix
            The prefix to prepend to fractional variables. If `None` a default
            prefix of `'frac_'` is used.
        """
        super().__init__(denominator=denominator, frac_prefix=frac_prefix)
        if isinstance(variables, str):
            self._variables = [variables]
        else:
            self._variables = list(variables)

    def variables_to_download(self) -> List[str]:
        """
        Return a list of the variables that need to be downloaded from the U.S. Census API.

        This consists of the variables passed at construction time, and a denominator
        variable if one was specified.
        """
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
        """
        Post-process after downloading to compute variables like fractional variables are constructed.

        This is where fractional variables are generated.

        Parameters
        ----------
        df_downloaded
            A data frame of variables that were downloaded. Any systhesized variables
            are added as new columns.

        Returns
        -------
            None. Any additions are made in-place in `df_downloaded`.
        """
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
        """Are two `VariableList`'s equal."""
        if not isinstance(other, VariableList):
            return False

        return (
            sorted(self._variables) == sorted(other._variables)
            and self.denominator == other.denominator
        )


class CensusGroup(VariableSpec):
    """Specification of a group of variables to download from the U.S. Census API."""

    def __init__(
        self,
        group: Union[str, Iterable[str]],
        *,
        leaves_only: bool = False,
        denominator: Optional[str] = None,
        frac_prefix: Optional[str] = None,
    ):
        """
        Specification of a group of variables to download from the U.S. Census API.

        Parameters
        ----------
        group
        leaves_only
        denominator
            The denominator to divide by when constructing fractional variables.
            If `False` then no fractional variables are added. If the name of a
            variable, that variable will be downloaded and used as a denominator
            to compute fractional versions of all of the other variables. If `True`
            then the denominator will be computed as the sum of all the other
            variables.
        frac_prefix
            The prefix to prepend to fractional variables. If `None` a default
            prefix of `'frac_'` is used.
        """
        if denominator is None:
            denominator = False

        super().__init__(denominator=denominator, frac_prefix=frac_prefix)
        self._group = [group] if isinstance(group, str) else list(group)
        self._leaves_only = leaves_only

    def groups_to_download(self) -> List[Tuple[str, bool]]:
        """
        Return the names of groups of variables that need to be downloaded from the U.S. Census API.

        The returned value are simply the groups specificed at construction time.

        Returns
        -------
            The names of groups to download.
        """
        return [(group, self._leaves_only) for group in self._group]

    def synthesize(self, df_downloaded: Union[pd.DataFrame, gpd.GeoDataFrame]):
        """
        Post-process after downloading to compute variables like fractional variables are constructed.

        This is where fractional variables are generated.

        Parameters
        ----------
        df_downloaded
            A data frame of variables that were downloaded. Any systhesized variables
            are added as new columns.

        Returns
        -------
            None. Any additions are made in-place in `df_downloaded`.
        """
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
        """Are two `CensusGroup`'s equal."""
        if not isinstance(other, CensusGroup):
            return False

        return (
            sorted(self._group) == sorted(other._group)
            and self.denominator == other.denominator
            and self._leaves_only == other._leaves_only
        )


class VariableSpecCollection(VariableSpec):
    """Specification built on top of a collection of other :py:class:`~VariableSpec`s."""

    def __init__(self, variable_specs: Iterable[VariableSpec]):
        super().__init__(denominator=None)
        self._variable_specs = list(variable_specs)

    def variables_to_download(self) -> List[str]:
        """
        Return a list of the variables that need to be downloaded from the U.S. Census API.

        Returns all the variables to be downloaded by the :py:class:`~VariableSpec`'s
        in the collection.
        """
        return list(
            set(
                itertools.chain(
                    *[spec.variables_to_download() for spec in self._variable_specs]
                )
            )
        )

    def groups_to_download(self) -> List[Tuple[str, bool]]:
        """
        Return the names of groups of variables that need to be downloaded from the U.S. Census API.

        The result is a list of the unique groups returned by all the :py:class:`~VariableSpec`'s
        given at construction time.

        Returns
        -------
            The names of groups to download.
        """
        return list(
            set(
                itertools.chain(
                    *[spec.groups_to_download() for spec in self._variable_specs]
                )
            )
        )

    def synthesize(self, df_downloaded: Union[pd.DataFrame, gpd.GeoDataFrame]):
        """
        Post-process after downloading to compute variables like fractional variables are constructed.

        We do this by calling `synthesize` on each of our constituent variable specifications.

        Parameters
        ----------
        df_downloaded
            A data frame of variables that were downloaded. Any systhesized variables
            are added as new columns.

        Returns
        -------
            None. Any additions are made in-place in `df_downloaded`.
        """
        df = df_downloaded
        for spec in self._variable_specs:
            spec.synthesize(df)

    def __eq__(self, other) -> bool:
        """Are two `VariableSpecCollection`s equal."""
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
    """A specification for what data we want from the U.S. Census API."""

    def __init__(
        self,
        dataset: str,
        vintage: VintageType,
        specs: Union[VariableSpec, Iterable[VariableSpec]],
        geography: Dict[str, Union[str, List[str]]],
        *,
        with_geometry: bool = False,
        remove_water: bool = False,
    ):
        """
        Construct a specification for what data we want from the U.S. Census API.

        In order to download data we must know the data set and vintage
        and have one or more :py:class:`~VariableSpec`s that tell us
        what variables we need and what synthetic variables to create,
        for example fractional variables.

        Parameters
        ----------
        dataset
            The dataset to download from. For example `"acs/acs5"`,
            `"dec/pl"`, or `"timeseries/poverty/saipe/schdist"`. There are
            symbolic names for datasets, like `ACS5` for `"acs/acs5"
            in :py:module:`censusdis.datasets`.
        vintage
            The vintage to download data for. For most data sets this is
            an integer year, for example, `2020`.        specs
        geography
            A specification of the geography, for example `{'state': '*'}`
            for all states or `{'state': censusdis.states.NJ, 'county': '*'}`
            for all counties in New Jersey.
        with_geometry
            If `True` a :py:class:`gpd.GeoDataFrame` will be returned and each row
            will have a geometry that is a cartographic boundary suitable for platting
            a map. See https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
            for details of the shapefiles that will be downloaded on your behalf to
            generate these boundaries.
        remove_water
            If `True` and if with_geometry=True, will query TIGER for AREAWATER shapefiles and
            remove water areas from returned geometry.
        """
        # Map symbolic names or use what we are given if there is no mapping.
        self._dataset = getattr(censusdis.datasets, dataset, dataset)
        self._vintage = vintage
        # If it is a raw list construct a collection around it.
        self._variable_spec = (
            specs if isinstance(specs, VariableSpec) else VariableSpecCollection(specs)
        )
        self._geography = self.map_state_names(geography)
        self._with_geometry = with_geometry
        self._remove_water = remove_water

    @classmethod
    def map_state_names(
        cls, geography: Dict[str, Union[str, List[str]]]
    ) -> Dict[str, Union[str, List[str]]]:
        """If there is a state in a geography, try to map it."""

        def map_state(state: str) -> str:
            """Map the name if a symbolic name exists."""
            return getattr(censusdis.states, state, state)

        # If there is no 'state' in geography there is nothing to do.
        # If there is a 'state', we copy the dict and do the mapping.
        if "state" in geography:
            geography = dict(geography)
            if isinstance(geography["state"], str):
                geography["state"] = map_state(geography["state"])
            else:
                geography["state"] = [map_state(state) for state in geography["state"]]

        return geography

    @property
    def dataset(self) -> str:
        """What data set to query."""
        return self._dataset

    @property
    def vintage(self) -> VintageType:
        """What vintage."""
        return self._vintage

    @property
    def with_geometry(self) -> bool:
        """Do we want to download geometry as well as data so we can plot maps."""
        return self._with_geometry

    @property
    def remove_water(self) -> bool:
        """Should we improve the geometry by masking off water."""
        return self._remove_water

    @property
    def variable_spec(self) -> VariableSpec:
        """The specification of variables to download."""
        return self._variable_spec

    @property
    def geography(self) -> Dict[str, Union[str, List[str]]]:
        """What geography to download data for."""
        return self._geography

    def download(
        self,
        api_key: Optional[str] = None,
    ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        """
        Download the data we want from the U.S. Census API.

        Parameters
        ----------
        api_key
            An optional API key. If you don't have or don't use a key, the number
            of calls you can make will be limited to 500 per day.

        Returns
        -------
            A :py:class:`~pd.DataFrame` or `~gpd.GeoDataFrame` containing the requested US Census data.
        """
        return self._variable_spec.download(
            dataset=self.dataset,
            vintage=self._vintage,
            with_geometry=self._with_geometry,
            remove_water=self._remove_water,
            api_key=api_key,
            **self._geography,
        )

    @classmethod
    def _yaml_loader(cls):
        loader = VariableSpec._yaml_loader()
        loader.add_constructor("!DataSpec", _class_constructor(cls))
        return loader

    @classmethod
    def load_yaml(cls, path: Union[str, Path]):
        """Load a YAML file containing a `DataSpec`."""
        loader = cls._yaml_loader()

        loaded = yaml.load(open(path, "rb"), Loader=loader)

        return loaded


class PlotSpec:
    """A specification for how to plot data we downloaded."""

    def __init__(
        self,
        *,
        variable: Optional[str] = None,
        boundary: bool = False,
        with_background: bool = False,
        plot_kwargs: Optional[Dict[str, Any]] = None,
        projection: Optional[str] = None,
    ):
        """
        Specify how to plot data we downloaded.

        Parameters
        ----------
        variable
            What variable to plot. Specify this to shade geographies
            based on the value of the variable. Leave out and set `boundary=True`
            to plot boundaries instead.
        boundary
            Should we plot boundaries instead of filled geographies?
            If `True`, `variable` should not be speficied.
        with_background
        plot_kwargs
        projection
        """
        if variable is None and not boundary:
            raise ValueError("Must specify either `variable=` or `boundary=True`")
        if variable is not None and boundary:
            raise ValueError("Must specify only one of `variable=` or `boundary=True`")

        self._variable = variable
        self._boundary = boundary
        self._with_background = with_background
        if plot_kwargs is None:
            plot_kwargs: Dict[str, Any] = {}
        self._plot_kwargs = plot_kwargs
        self._projection = projection

    @property
    def variable(self) -> Union[str, None]:
        """What variable will we plot."""
        return self._variable

    @property
    def boundary(self) -> bool:
        """Should we plot boundaries instead of a variable."""
        return self._boundary

    @property
    def with_background(self) -> bool:
        """Should we plot a background map from Open Street Maps."""
        return self._with_background

    @property
    def plot_kwargs(self) -> Dict[str, Any]:
        """
        Additional keyword args to control the plot.

        e.g. `{'figsize': [12, 8]} to change the default size of the plot.
        """
        return self._plot_kwargs

    @property
    def projection(self):
        """What projection to use when plotting."""
        return self._projection

    def __eq__(self, other) -> bool:
        """Are two `PlotSpec`'s equal."""
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
        """
        Plot data on a map according to the specification.

        Parameters
        ----------
        gdf
            The data to plot.

        Returns
        -------
            `ax` of the plot.
        """
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
    def _yaml_loader(cls):
        loader = yaml.SafeLoader
        loader.add_constructor("!PlotSpec", _class_constructor(cls))
        return loader

    @classmethod
    def load_yaml(cls, path: Union[str, Path]) -> "PlotSpec":
        """Load a YAML file containing a `PlotSpec`."""
        loader = cls._yaml_loader()

        loaded = yaml.load(open(path, "rb"), Loader=loader)

        return loaded
