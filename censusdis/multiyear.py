"""Utility functions for downloading, graphing and analyzing multiple years of ACS data."""

from collections import defaultdict
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import censusdis.data as ced
from censusdis.datasets import ACS1, ACS3, ACS5

import re

from typing import List, Optional, Union, Iterable, Callable, Dict


def is_variable_column(
    col: str,
    download_variables: Optional[Union[str, Iterable[str]]],
    group: Optional[str],
) -> bool:
    """
    Determine whether a column is a Census variable.

    There are two ways to download data from the Census Bureau: as a group (i.e. table) or
    as a list of variables. The way to test whether a column of the resulting
    df is a variable depends on whether the data was requested by group or variable.

    In practice this function is used to drop columns that contain metadata that I don't need.
    We want columns like "B01001_001E" and not like "STATE"
    """
    if group and col.startswith(group):
        return True
    if download_variables and col in download_variables:
        return True

    return False


# This function is based on the notebook linked to in this github issue:
# https://github.com/censusdis/censusdis/issues/325
def name_mapper(
    dataset: str,
    vintage: int,
    download_variables: Optional[Union[str, Iterable[str]]],
    group: Optional[str],
) -> Callable[[str], str]:
    """Return a function that converts an ACS variable to its label."""

    def inner(variable: str) -> str:
        """Map from the variables we got back to their labels."""
        if is_variable_column(variable, download_variables, group):
            # Look up details of the particular variable:
            vars = ced.variables.search(
                dataset, vintage, group_name=group, name=variable
            )
            # Census uses !! to indicate nesting of Labels. Ex. 'Estimate!!Total:'
            # We care about the last part.
            label = vars.iloc[0]["LABEL"]
            label = re.split(r"!!", label)[-1]

            # Starting in 2020 Labels which are parents of other Labels have a : as a suffix.
            # See an example here: https://data.census.gov/table?q=country%20of%20birth&g=9700000US3612510
            # (Ex. "Total:", "Asia:", "Eastern Asia:", "China:")
            # For my purposes, it is better to drop this trailing :
            return label[:-1] if label[-1] == ":" else label
        else:
            # Not in the group we are interested in, so leave it as is.
            return variable

    return inner


def get_unique_labels_for_variable(
    acs: str, variable: str, years: List[int]
) -> Dict[str, List[int]]:
    """
    Return all labels the ACS has used for a given variable.

    Note that the ACS sometimes changes the labels of a variable. Sometimes these changes are minor,
    and sometimes the same variable is used for something completely different. This function is designed to
    facilitate doing this check over multiple years.

    For example, B08006_017E in 2005 had label 'Estimate!!Total!!Motorcycle'. But in 2006 it switched to
    'Estimate!!Total!!Worked at home'. And in 2019 it changed to 'Estimate!!Total:!!Worked from home'.

    To reduce false positives labels are converted to lower case prior to comparison ("Race" is
    inconsistently capitalized over the years). Also, all ":" are removed prior to comparison so that
    "estimate!!total:!!native" is the same as "estimate!!total!!native".

    Parameters
    ----------
    - acs: The ACS to use. Ex. censusdis.datasets.ACS1
    - variable: The variable in question. Ex. 'B01001_001E'
    - years: An iterable of years to use. Ex. [2005, 2006, 2007]

    Returns
    -------
    - A dict where each key is a label, and each value is a list of years that key has been used.

    Note: If the dict returned is of length 1, then the variable has only ever had 1 label.
    """
    labels = defaultdict(list)

    for year in years:
        label = ced.variables.get(acs, year, variable)["label"].lower()
        label = label.replace(":", "")

        labels[label].append(year)

    return labels


class VariableMistmatchOverTimeError(Exception):
    """Raised when an ACS variable has had multiple labels over time."""

    pass


def warn_variable_changes(
    df: pd.DataFrame,
    dataset: str,
    vintages: List[int],
    download_variables: Optional[Union[str, Iterable[str]]],
    group: Optional[str],
    prompt: bool,
) -> None:
    """
    Issue a warning when an ACS variable has had multiple labels over the years.

    In the ACS, Sometimes the same variable is used for different things in different years.
    For example in 2005 `B08006_017E` was used for "Estimate!!Total!!Motorcycle". But in 2006 it
    changed to "Estimate!!Total!!Worked at home" and in 2019 it changed to "Estimate!!Total:!!Worked from home".
    This code alerts users of any variables which have had different labels over time.

    This function always emits a warning if it encounters that situation. If prompt is True
    then it also prompts the user to confirm whether they want to continue with the download.
    """
    years = df["Year"].unique()

    for col in df.columns:
        if not is_variable_column(col, download_variables, group):
            continue

        unique_labels_for_variable = get_unique_labels_for_variable(
            dataset, col, vintages
        )

        if len(unique_labels_for_variable) > 1:
            print(f"Warning: {col} has had multiple labels over the selected years:")
            for label, years in unique_labels_for_variable.items():
                print(f"\t'{label}' in {years}")
            if prompt:
                if input("Continue downloading dataset (y/n)?") != "y":
                    raise VariableMistmatchOverTimeError()


def download_multiyear(
    dataset: str,
    vintages: List[int],
    download_variables: Optional[Union[str, Iterable[str]]] = None,
    *,
    group: Optional[str] = None,
    rename_vars: bool = True,
    drop_cols: bool = True,
    prompt: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """
    Download multiple years of ACS data into a single dataframe.

    Variables can be specified individually by `download_variables` or as a table by `group`.

    Parameters
    ----------
    dataset
        Must be one of `censusdis.datasets.ACS1`, `censudis.datasets.ACS3` or `censusdis.datasets.ACS5`.
    vintages
        A list of years to download data for.
    download_variables
        The census variables to download, for example `["NAME", "B01001_001E"]`.
    group
        One or more groups (as defined by the U.S. Census for the data set)
        whose variable values should be downloaded.
    rename_vars
        If True, rename the columns from variables (ex. "B01001_001E") to their labels (ex. "Total").
        The labels for the last year are used.
    drop_cols
        If True, drop cols that do not contain variables or the year (ex. geography columns).
    prompt
        This function emits a warning each time a downloaded variable has had multiple labels over time.
        If True, prompt the user whether they want to continue downloading the dataset despite the differences.
    **kwargs
        Geography parameters passed directly to `ced.download`.

    Returns
    -------
    A dataframe.

    Examples
    --------
    # Download the population by nativity in Great Neck School District, NY.
    from censusdis.multiyear import download_multiyear
    from censusdis.datasets import ACS5
    from censusdis.states import NY

    # Download the entire table.
    df = download_multiyear(
        dataset=ACS5,
        vintages=[2009, 2014, 2019],
        group="B05012",
        prompt=False,
        state=NY,
        school_district_unified="12510",
    )

    # Downloaded selected variables.
    df = download_multiyear(
        dataset=ACS5,
        vintages=[2009, 2014, 2019],
        download_variables=["B05006_049E", "B05006_060E", "B05006_054E"],
        state=NY,
        school_district_unified="12510",
        drop_cols=True,
    )
    """
    if dataset not in [ACS1, ACS3, ACS5]:
        raise ValueError(
            "Dataset must be one of `censusdis.datasets.ACS1`, `censusdis.datasets.ACS3` or `censusdis.datasets.ACS5`"
        )

    if (download_variables is None and group is None) or (
        download_variables is not None and group is not None
    ):
        raise ValueError("Exactly one of download_variables and group must be set.")

    df = None

    for vintage in vintages:
        # This loop can take a while, so provide feedback to the user
        print(".", end="", flush=True)

        df_new = ced.download(
            dataset=dataset,
            vintage=vintage,
            download_variables=download_variables,
            group=group,
            **kwargs,
        )

        df_new["Year"] = vintage

        if df is None:
            df = df_new
        else:
            df = pd.concat([df, df_new])

    warn_variable_changes(df, dataset, vintages, download_variables, group, prompt)

    if drop_cols:
        df = df[
            [
                col
                for col in df.columns
                if is_variable_column(col, download_variables, group) or col == "Year"
            ]
        ]

    if rename_vars:
        df = df.rename(
            columns=name_mapper(
                dataset=dataset,
                vintage=vintages[-1],
                download_variables=download_variables,
                group=group,
            )
        )

    df = df.reset_index(drop=True)
    return df


def graph_multiyear(
    df: pd.DataFrame,
    title: str = "",
    yaxis_title: str = "",
    y_cols: Optional[Iterable[str]] = None,
) -> None:
    """
    Create a (multi-line) graph of time series data.

    Parameters
    ----------
    df
        Must have a column called 'Year' which will serve as the x-axis.
    title
        Title for the graph.
    yaxis_title
        Title for the y-axis.
    y_cols
        A list of columns in `df` to create lines for. If None then will graph all
        columns except "Year".

    Returns
    -------
    NoneType

    Examples
    --------
    # Graph the population by nativity in Great Neck School District, NY.
    from censusdis.multiyear import download_multiyear, graph_multiyear
    from censusdis.datasets import ACS5
    from censusdis.states import NY

    df = download_multiyear(
        dataset=ACS5,
        vintages=[2010, 2015, 2020],
        group="B05012",
        state=NY,
        school_district_unified="12510",
    )
    graph_multiyear(
        df,
        "Population by Nativity in Great Neck School District",
        "Population",
        ["Total", "Native", "Foreign-Born"],
    )
    """

    # Define a function to format the y-axis with commas
    def format_yaxis(value, tick_position):
        return f"{value:,.0f}"

    if not y_cols:
        y_cols = [col for col in df.columns if col != "Year"]

    colorblind_palette = [
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
        "#999999",
        "#E41A1C",
    ]

    for idx, y_col in enumerate(y_cols):
        plt.plot(
            df["Year"],
            df[y_col],
            label=y_col,
            marker="o",
            color=colorblind_palette[idx],
        )

    # Explicitly set the x-axis ticks to match the actual years in the data
    plt.xticks(ticks=df["Year"], labels=df["Year"], rotation=-45)

    # Apply comma formatting to the y-axis
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_yaxis))

    plt.xlabel("Year")
    plt.ylabel(yaxis_title)
    plt.title(title)
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.show()


def pct_change_multiyear(df: pd.DataFrame) -> pd.DataFrame:
    r"""
    Convert a multi-year dataframe from raw counts to percent change.

    Essentially runs pd.DataFrame.pct_change on all columns of the dataframe except the "Year" column.
    Rounds the results to 1 decimal point.

    Parameters
    ----------
    df
        Must have a column called 'Year'.

    Returns
    -------
    A Dataframe

    Examples
    --------
    # Graph the percent change in the population by nativity in Great Neck School District, NY.
    from censusdis.multiyear import (
        download_multiyear,
        pct_change_multiyear,
        graph_multiyear,
    )
    from censusdis.datasets import ACS5
    from censusdis.states import NY

    df = download_multiyear(
        dataset=ACS5,
        vintages=[2010, 2015, 2020],
        group="B05012",
        prompt=False,
        state=NY,
        school_district_unified="12510",
    )

    df = pct_change_multiyear(df)
    print(df)

    graph_multiyear(
        df,
        "Percent Change in Population by Nativity\nGreat Neck School District, NY",
        "Percent Change",
    )
    """
    years = df["Year"]

    df = df.pct_change() * 100
    df = df.round(1)

    df["Year"] = years

    return df
