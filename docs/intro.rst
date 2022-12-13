Getting Started
===============

Once you have :ref:`installed <installation>` ``censusdis`` in your Python
environment, you are ready to start using it.

Making Your First Query
-----------------------

Let's start with a simple example. We will use ``censusis.data``
to load the population of every state in the country from
the 2020 US Census redistricting data. In Census terms, the
name of dataset we want to use is `"dec/pl" <https://api.census.gov/data/2020/dec/pl.html>`_  and the name
of the variable we want to load is
`"P2_001N" <https://api.census.gov/data/2020/dec/pl/variables/P2_001N.html>`_.
``censusdis`` has APIs to explore and discover variables, but
for now, let's just assume we already knew what data set and
variable we wanted.

We can load the data as follows::

    import censusdis.data as ced

    DATASET = "dec/pl"
    YEAR = 2020
    VARIABLES = ["NAME", "P2_001N"]

    df_states = ced.download_detail(
        DATASET,
        YEAR,
        VARIABLES,
        state="*",
    )

The call
to ``ced.download_detail`` will construct
a URL in the Census API's preferred format
(``https://api.census.gov/data/2020/dec/pl?get=NAME,P2_001N&for=state:*``),
make a
request to the Census servers at that URL, parse the JSON that is
returned, and turn it into a ``pandas.DataFrame``.

``df_states`` now has the
name and population of all 50 states and the District of
Columbia. If we print it, it looks like::

       STATE                  NAME   P2_001N
    0     42          Pennsylvania  13002700
    1     06            California  39538223
    2     54         West Virginia   1793716
    3     49                  Utah   3271616
    4     36              New York  20201249
    5     11  District of Columbia    689545
    6     02                Alaska    733391
    7     12               Florida  21538187
    8     45        South Carolina   5118425
    9     38          North Dakota    779094
    10    23                 Maine   1362359
    11    13               Georgia  10711908
    12    01               Alabama   5024279
    13    33         New Hampshire   1377529
    14    41                Oregon   4237256
    15    56               Wyoming    576851
    16    04               Arizona   7151502
    17    22             Louisiana   4657757
    18    18               Indiana   6785528
    19    16                 Idaho   1839106
    20    09           Connecticut   3605944
    21    15                Hawaii   1455271
    22    17              Illinois  12812508
    23    25         Massachusetts   7029917
    24    48                 Texas  29145505
    25    30               Montana   1084225
    26    31              Nebraska   1961504
    27    39                  Ohio  11799448
    28    08              Colorado   5773714
    29    34            New Jersey   9288994
    30    24              Maryland   6177224
    31    51              Virginia   8631393
    32    50               Vermont    643077
    33    37        North Carolina  10439388
    34    05              Arkansas   3011524
    35    53            Washington   7705281
    36    20                Kansas   2937880
    37    40              Oklahoma   3959353
    38    55             Wisconsin   5893718
    39    28           Mississippi   2961279
    40    29              Missouri   6154913
    41    26              Michigan  10077331
    42    44          Rhode Island   1097379
    43    27             Minnesota   5706494
    44    19                  Iowa   3190369
    45    35            New Mexico   2117522
    46    32                Nevada   3104614
    47    10              Delaware    989948
    48    72           Puerto Rico   3285874
    49    21              Kentucky   4505836
    50    46          South Dakota    886667
    51    47             Tennessee   6910840

Notice that the data frame has three columns, ``"STATE"``,
``"NAME"``, and ``"P2_001N"``. The second and third are
what we asked for. But what about the first one, ``"STATE"``?
That is additional data that indicates the state
of each row, specified in terms of a
`FIPS Code <https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code#FIPS_state_codes>`_.
FIPS codes are two-digit strings that the Census
uses to identify states.

``censusdis`` returns FIPS codes like these to
you because they tend to be very useful in cases where
you might want to join this data with other data, either
from other ``censusdis`` queries or from other sources.
Joining on a FIPS code is usually more reliable and less
error-prone than joining on a string like the name of
a state. One data set might use the name "N. Carolina"
and another one might use "North Carolina", and a third
might use "NC". FIPS codes help us avoid confusion or
the need to keep mapping between them.

The states are in no particular order other than
what the underlying US Census API returned to us.
If order matters to you, you can sort the dataframe
by whatever column(s) you like, such as by the name
of the state, or by the population.

Filtering Queries
-----------------

Our first query got the population of every state.
Sometimes, especially when we are working at a smaller
level of granularity like a county, we don't want the
data for the whole country. We might want it just for
the counties of a particular state, say New Jersey.
In that case, we can specify this with additional
arguments to ``ced.download_detail``. For example::

    import censusdis.data as ced
    from censusdis.states import STATE_NJ

    DATASET = "dec/pl"
    YEAR = 2020
    VARIABLES = ["NAME", "P2_001N"]

    df_counties = ced.download_detail(
        DATASET,
        YEAR,
        VARIABLES,
        state=STATE_NJ,
        county="*",
    )

This query returns the following dataframe::

       STATE COUNTY                           NAME  P2_001N
    0     34    003      Bergen County, New Jersey   955732
    1     34    009    Cape May County, New Jersey    95263
    2     34    015  Gloucester County, New Jersey   302294
    3     34    021      Mercer County, New Jersey   387340
    4     34    027      Morris County, New Jersey   509285
    5     34    033       Salem County, New Jersey    64837
    6     34    039       Union County, New Jersey   575345
    7     34    001    Atlantic County, New Jersey   274534
    8     34    005  Burlington County, New Jersey   461860
    9     34    007      Camden County, New Jersey   523485
    10    34    011  Cumberland County, New Jersey   154152
    11    34    013       Essex County, New Jersey   863728
    12    34    017      Hudson County, New Jersey   724854
    13    34    019   Hunterdon County, New Jersey   128947
    14    34    023   Middlesex County, New Jersey   863162
    15    34    025    Monmouth County, New Jersey   643615
    16    34    029       Ocean County, New Jersey   637229
    17    34    031     Passaic County, New Jersey   524118
    18    34    035    Somerset County, New Jersey   345361
    19    34    037      Sussex County, New Jersey   144221
    20    34    041      Warren County, New Jersey   109632

Note that in this case, we received both the FIPS code for
the state (34 in New Jersey) and the county within the state,
along with the name of the county and its population. The
same county FIPS codes are reused from one state to the
next, so if we wanted to join this with data from elsewhere
we would need to join on both the state FIPS code and the
county FIPS code. Note also that joining by NAME could
get really messy. Is "Bergen CNTY, NJ" the same as
"Bergen County, New Jersey"?

Since the first two queries we did both went to the same
underlying "dec/pl" dataset, the numbers they contain
should add up. We can verify this by seeing if the total
population of all the counties in New Jersey in the second
query is equal to the population of the state from the
first query with::

    df_counties['P2_001N'].sum()

Sure enough, this sum is ``9288994``, exactly what we
saw in the New Jersey row of ``df_states``.

Additional Geographies
----------------------

Depending on what dataset we are querying, data may
be available at a wide variety of geographic levels.
Some, like region, are very large. In the US Census
data model, there are only four regions. Their populations
can be queried with::

    import censusdis.data as ced

    DATASET = "dec/pl"
    YEAR = 2020
    VARIABLES = ["NAME", "P2_001N"]

    df_region = ced.download_detail(
        DATASET,
        YEAR,
        VARIABLES,
        region="*",
    )

The result is::

      REGION              NAME    P2_001N
    0      2    Midwest Region   68985454
    1      3      South Region  126266107
    2      4       West Region   78588572
    3      1  Northeast Region   57609148

On the other hand, we can go down to very small
geographies called *block groups*. These are
small neighborhoods of just a few blocks, each of
which is typically home to
somewhere between hundreds and thousands of
people. Here is
a block group query for Essex County, NJ::

    import censusdis.data as ced
    from censusdis.states import STATE_NJ

    COUNTY_ESSEX_NJ = "013" # See county query above.

    DATASET = "dec/pl"
    YEAR = 2020
    VARIABLES = ["NAME", "P2_001N"]

    df_bg = ced.download_detail(
        DATASET,
        YEAR,
        VARIABLES,
        state=STATE_NJ,
        county=COUNTY_ESSEX_NJ,
        block_group="*",
    )

The results of this are much larger than our previous
dataframes. There are 672 block groups in the county.
The results (leaving out a bunch of rows in the middle)
look like::

        STATE COUNTY   TRACT BLOCK_GROUP                                                             NAME  P2_001N
    0      34    013  000100           2      Block Group 2, Census Tract 1, Essex County, New Jersey         2104
    1      34    013  000200           2      Block Group 2, Census Tract 2, Essex County, New Jersey         2096
    2      34    013  000400           1      Block Group 1, Census Tract 4, Essex County, New Jersey         2514
    3      34    013  000600           1      Block Group 1, Census Tract 6, Essex County, New Jersey         1816
    4      34    013  000700           2      Block Group 2, Census Tract 7, Essex County, New Jersey         2469
    5      34    013  000800           1      Block Group 1, Census Tract 8, Essex County, New Jersey         2388
    6      34    013  000900           1      Block Group 1, Census Tract 9, Essex County, New Jersey         1960
    7      34    013  001000           1      Block Group 1, Census Tract 10, Essex County, New Jersey        1100
    8      34    013  001100           2      Block Group 2, Census Tract 11, Essex County, New Jersey        1228
    9      34    013  001400           2      Block Group 2, Census Tract 14, Essex County, New Jersey        1742

    ...

    662    34    013  004700           2      Block Group 2, Census Tract 47, Essex County, New Jersey        1086
    663    34    013  004700           3      Block Group 3, Census Tract 47, Essex County, New Jersey         772
    664    34    013  004700           4      Block Group 4, Census Tract 47, Essex County, New Jersey         894
    665    34    013  004700           5      Block Group 5, Census Tract 47, Essex County, New Jersey         913
    666    34    013  004801           1      Block Group 1, Census Tract 48.01, Essex County, New Jersey     1681
    667    34    013  004801           2      Block Group 2, Census Tract 48.01, Essex County, New Jersey      912
    668    34    013  004802           1      Block Group 1, Census Tract 48.02, Essex County, New Jersey     1899
    669    34    013  004802           2      Block Group 2, Census Tract 48.02, Essex County, New Jersey      563
    670    34    013  004802           3      Block Group 3, Census Tract 48.02, Essex County, New Jersey     1651
    671    34    013  004900           1      Block Group 1, Census Tract 49, Essex County, New Jersey        1052

An interesting thing happened here. We asked for all the
block groups in the county. ``censusdis`` was smart
enough to realize that block groups are nested inside
geographies called census tracts, that are in turn nested
inside counties. In order to give us enough identifiers
to unambiguously differentiate the rows, the "TRACT"
column was added even though we did not mention it in
our query. As you can see in the results, the block group
identifier is typically a single digit number, but is
unique within a tract.

If you want to find out what all the supported geographies
for a data set are, you can check a US Census page like
https://api.census.gov/data/2020/dec/pl/geography.html, which
is normally linked from the page describing the dataset
(https://api.census.gov/data/2020/dec/pl.html in this case).

``censusdis`` queries the same geography data that powers
these pages so that it can tell you what options are available
and how, in python, to specify them as arguments. You can
look at this information with the following code::

    import censusdis.geography as cgeo

    DATASET = "dec/pl"
    YEAR = 2020

    specs = cgeo.geo_path_snake_specs(DATASET, YEAR)

``specs`` will now contain::

    {'010': ['us'],
     '020': ['region'],
     '030': ['division'],
     '040': ['state'],
     '050': ['state', 'county'],
     '060': ['state', 'county', 'county_subdivision'],
     '067': ['state', 'county', 'county_subdivision', 'subminor_civil_division'],
     '100': ['state', 'county', 'tract', 'block'],
     '140': ['state', 'county', 'tract'],
     '150': ['state', 'county', 'tract', 'block_group'],

     ...

     '330': ['combined_statistical_area'],

     ...

     '745': ['state',
             'county',
             'voting_district',
             'county_subdivision_or_part',
             'subminor_civil_division_or_part',
             'tract_or_part',
             'block_group_or_part'],
     '950': ['state', 'school_district_elementary'],
     '960': ['state', 'school_district_secondary'],
     '970': ['state', 'school_district_unified']}

mirroring what was on the web site, but in a form that
additional code can more easily digest. Note that the
queries we performed so far corresponded to geographies
``'040'``, ``'020'``, and ``150``. In all cases,
``censusdis`` chose the least specific geography that
could be matched against the keyword arguments we
provided.

We can query any of these geographies we like, using the
argument naming conventions returned in ``specs`` above.
For example::

    import censusdis.data as ced

    DATASET = "dec/pl"
    YEAR = 2020
    VARIABLES = ["NAME", "P2_001N"]

    df_csa = ced.download_detail(
        DATASET,
        YEAR,
        VARIABLES,
        combined_statistical_area="*"
    )

which produces the results::

      COMBINED_STATISTICAL_AREA                                                     NAME  P2_001N
    0                       104                               Albany-Schenectady, NY CSA  1190727
    1                       106                   Albuquerque-Santa Fe-Las Vegas, NM CSA  1162523
    2                       107                               Altoona-Huntingdon, PA CSA   166914
    3                       108                            Amarillo-Pampa-Borger, TX CSA   311362
    4                       118                          Appleton-Oshkosh-Neenah, WI CSA   414877
    5                       120                         Asheville-Marion-Brevard, NC CSA   546579
    6                       122  Atlanta--Athens-Clarke County--Sandy Springs, GA-AL CSA  6930423
    7                       140                                  Bend-Prineville, OR CSA   222991
    8                       142                      Birmingham-Hoover-Talladega, AL CSA  1350646
    9                       144                              Bloomington-Bedford, IN CSA   206050

    ...

    165                     539                                   Tupelo-Corinth, MS CSA   198138
    166                     540                               Tyler-Jacksonville, TX CSA   283891
    167                     544                             Victoria-Port Lavaca, TX CSA   118437
    168                     545                        Virginia Beach-Norfolk, VA-NC CSA  1890162
    169                     548       Washington-Baltimore-Arlington, DC-MD-VA-WV-PA CSA  9973383
    170                     554            Wausau-Stevens Point-Wisconsin Rapids, WI CSA   311012
    171                     556                                 Wichita-Winfield, KS CSA   682159
    172                     558                          Williamsport-Lock Haven, PA CSA   151638
    173                     566                             Youngstown-Warren, OH-PA CSA   643120
    174                     517                              Spencer-Spirit Lake, IA CSA    34087

for the 175 CSAs in the US.

More Variables
--------------

So far, we have only been looking at the variables
``'NAME'`` and ``'P2_001N'`` from the ``'dec/pl'``
dataset. But there are thousands of other interesting
variables in various data sets you might want to look at.

In many data sets, variables are organized into
groups. ``censusdis`` has APIs to explore groups
of related variables and load the ones you are
most interested in. There is an example in the
`SoMa DIS Demo <./nb/SoMa%20DIS%20Demo.html>`_
notebook, which looks at racial demographics and
computes diversity and integration metrics at the
census tract level.

Aside from ``"dev/pl"``, you might want to look at the
`American Community Survey (ACS) <https://www.census.gov/programs-surveys/acs>`_
data sets. There is a
demo of how to load and use ACS 5-year survey
data in the `ACS Demo <./nb/ACS%20Demo.html>`_
notebook.

One way to explore variables is to look at groups
of variables. We did a little bit of this in the
`SoMa DIS Demo <./nb/SoMa%20DIS%20Demo.html>`_
notebook. We do some more rigorous analysis of
groups and variables in the
`SoMa DIS Demo <./nb/Exploring%20Variables.html>`_
notebook.

Additional Examples in Notebooks
--------------------------------

There are additional more advanced examples and
additional maps and visualizations,
presented in more `Demo Notebooks <./notebooks.html>`_.

Help and Issues
---------------

If you have questions or want to report a bug or
feature request, please contact us by opening an issue
at https://github.com/vengroff/censusdis/issues.