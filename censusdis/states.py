# Copyright (c) 2022 Darren Erik Vengroff

"""
Defines state FIPS codes and some utilities for using them.

The US Census identifies states by their
`FIPS Codes <https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_code#FIPS_codes>`_,
which are two-digit numeric strings. For convenience, we
define identifiers for them.

Each identifier corresponds to the two
letter abbreviation for the state. For example, NJ
is the two letter abbreviation for New Jersey, and the
Census state identifier for New Jersey is 34, so::

    from censusdis import states

    state = states.NJ

would set the value of `state` to the string `"34"`.
We can use these values in any of the APIs in
`censusdis` that take a state.

There is also a dictionary whose keys are the state
FIPS codes and whose values are strings naming
the states. It is typically used when we want a
more human-friendly name for each state. As in::

    from censusdis import states

    state = states.CA

    print(
        f"The name of the state with ID '{state}' "
        f"is '{states.NAMES_FROM_IDS[state]}'."
    )

Finally, there is a list of all states. It is often useful
if we want to perform an operation on all states. For
example::

    from censusdis import states

    for state in states.ALL_STATES:
        do_something_with_a_state(state)

There is also a list that includes all states and the
District of Columbia. It is called ``ALL_STATES_AND_DC``.
And finally, ``ALL_STATES_AND_DC_AND_PR`` includes
Puerto Rico as well.
"""


AL = "01"
"""Alabama"""

AK = "02"
"""Alaska"""

AZ = "04"
"""Arizona"""

AR = "05"
"""Arkansas"""

CA = "06"
"""California"""

CO = "08"
"""Colorado"""

CT = "09"
"""Connecticut"""

DE = "10"
"""Delaware"""

DC = "11"
"""District of Columbia"""

FL = "12"
"""Florida"""

GA = "13"
"""Georgia"""

HI = "15"
"""Hawaii"""

ID = "16"
"""Idaho"""

IL = "17"
"""Illinois"""

IN = "18"
"""Indiana"""

IA = "19"
"""Iowa"""

KS = "20"
"""Kansas"""

KY = "21"
"""Kentucky"""

LA = "22"
"""Louisiana"""

ME = "23"
"""Maine"""

MD = "24"
"""Maryland"""

MA = "25"
"""Massachusetts"""

MI = "26"
"""Michigan"""

MN = "27"
"""Minnesota"""

MS = "28"
"""Mississippi"""

MO = "29"
"""Missouri"""

MT = "30"
"""Montana"""

NE = "31"
"""Nebraska"""

NV = "32"
"""Nevada"""

NH = "33"
"""New Hampshire"""

NJ = "34"
"""New Jersey--The Garden State"""

NM = "35"
"""New Mexico"""

NY = "36"
"""New York"""

NC = "37"
"""North Carolina"""

ND = "38"
"""North Dakota"""

OH = "39"
"""Ohio"""

OK = "40"
"""Oklahoma"""

OR = "41"
"""Oregon"""

PA = "42"
"""Pennsylvania"""

RI = "44"
"""Rhode Island"""

SC = "45"
"""South Carolina"""

SD = "46"
"""South Dakota"""

TN = "47"
"""Tennessee"""

TX = "48"
"""Texas"""

UT = "49"
"""Utah"""

VT = "50"
"""Vermont"""

VA = "51"
"""Virginia"""

WA = "53"
"""Washington"""

WV = "54"
"""West Virginia"""

WI = "55"
"""Wisconsin"""

WY = "56"
"""Wyoming"""

PR = "72"
"""Puerto Rico"""


NAMES_FROM_IDS = {
    AL: "Alabama",
    AK: "Alaska",
    AZ: "Arizona",
    AR: "Arkansas",
    CA: "California",
    CO: "Colorado",
    CT: "Connecticut",
    DC: "District of Columbia",
    DE: "Delaware",
    FL: "Florida",
    GA: "Georgia",
    HI: "Hawaii",
    ID: "Idaho",
    IL: "Illinois",
    IN: "Indiana",
    IA: "Iowa",
    KS: "Kansas",
    KY: "Kentucky",
    LA: "Louisiana",
    ME: "Maine",
    MD: "Maryland",
    MA: "Massachusetts",
    MN: "Minnesota",
    MS: "Mississippi",
    MI: "Michigan",
    MO: "Missouri",
    MT: "Montana",
    NE: "Nebraska",
    NV: "Nevada",
    NH: "New Hampshire",
    NJ: "New Jersey",
    NM: "New Mexico",
    NY: "New York",
    NC: "North Carolina",
    ND: "North Dakota",
    OH: "Ohio",
    OK: "Oklahoma",
    OR: "Oregon",
    PA: "Pennsylvania",
    RI: "Rhode Island",
    SC: "South Carolina",
    SD: "South Dakota",
    TN: "Tennessee",
    TX: "Texas",
    UT: "Utah",
    VT: "Vermont",
    VA: "Virginia",
    WA: "Washington",
    WV: "West Virginia",
    WI: "Wisconsin",
    WY: "Wyoming",
    PR: "Puerto Rico",
}
"""
The names of each state, indexed by FIPS code.

For example, ``NAMES_FROM_IDS[NJ]``
is ``"New Jersey"``.
"""

ABBREVIATIONS_FROM_IDS = {
    AL: "AL",
    AK: "AK",
    AZ: "AZ",
    AR: "AR",
    CA: "CA",
    CO: "CO",
    CT: "CT",
    DC: "DC",
    DE: "DE",
    FL: "FL",
    GA: "GA",
    HI: "HI",
    ID: "ID",
    IL: "IL",
    IN: "IN",
    IA: "IA",
    KS: "KS",
    KY: "KY",
    LA: "LA",
    ME: "ME",
    MD: "MD",
    MA: "MA",
    MN: "MN",
    MS: "MS",
    MI: "MI",
    MO: "MO",
    MT: "MT",
    NE: "NE",
    NV: "NV",
    NH: "NH",
    NJ: "NJ",
    NM: "NM",
    NY: "NY",
    NC: "NC",
    ND: "ND",
    OH: "OH",
    OK: "OK",
    OR: "OR",
    PA: "PA",
    RI: "RI",
    SC: "SC",
    SD: "SD",
    TN: "TN",
    TX: "TX",
    UT: "UT",
    VT: "VT",
    VA: "VA",
    WA: "WA",
    WV: "WV",
    WI: "WI",
    WY: "WY",
    PR: "PR",
}
"""
The postal abbreviation of each state, indexed by FIPS code.

For example, ``NAMES_FROM_IDS[NJ]``
is ``"NJ"``.
"""

IDS_FROM_ABBREVIATIONS = {v: k for k, v in ABBREVIATIONS_FROM_IDS.items()}
"""
The state FIPS code ID for each state abbreviation.

For example ``IDS_FROM_ABBREVIATIONS['NJ']``
is ``34``, which is the value of``NJ``.
"""

IDS_FROM_NAMES = {v: k for k, v in NAMES_FROM_IDS.items()}
"""
The state FIPS code ID for each state name.

For example ``IDS_FROM_ABBREVIATIONS['New Jersey']``
is ``34``, which is the value of``NJ``.
"""

ALL_STATES = [state for state in NAMES_FROM_IDS if state != DC and state != DC]
"""
All the state FIPS codes.

Includes all 50 states, but not DC.

Typically used to iterate over the states, as in::

    from censusdis.states import ALL_STATES

    for state in ALL_STATES:
        process_state(state)
"""

ALL_STATES_DC_AND_PR = list(NAMES_FROM_IDS.keys())
"""
All the state FIPS codes and DC and PR.

Includes all 50 states, DC and PR.

Typically used to iterate over the states, as in::

    from censusdis.states import ALL_STATES_DC_AND_PR

    for state in ALL_STATES_DC_AND_PR:
        process_state(state)
"""

ALL_STATES_AND_DC = [state for state in ALL_STATES_DC_AND_PR if state != PR]
"""
All the state FIPS codes and DC.

Includes all 50 states and DC.

Typically used to iterate over the states, as in::

    from censusdis.states import ALL_STATES_AND_DC

    for state in ALL_STATES_AND_DC:
        process_state(state)
"""

# Legacy names. These will go away some time before the 1.0.0 release.

STATE_AL = AL
STATE_AK = AK
STATE_AZ = AZ
STATE_AR = AR
STATE_CA = CA
STATE_CO = CO
STATE_CT = CT
STATE_DC = DC
STATE_DE = DE
STATE_FL = FL
STATE_GA = GA
STATE_HI = HI
STATE_ID = ID
STATE_IL = IL
STATE_IN = IN
STATE_IA = IA
STATE_KS = KS
STATE_KY = KY
STATE_LA = LA
STATE_ME = ME
STATE_MD = MD
STATE_MA = MA
STATE_MN = MN
STATE_MS = MS
STATE_MI = MI
STATE_MO = MO
STATE_MT = MT
STATE_NE = NE
STATE_NV = NV
STATE_NH = NH
STATE_NJ = NJ
STATE_NM = NM
STATE_NY = NY
STATE_NC = NC
STATE_ND = ND
STATE_OH = OH
STATE_OK = OK
STATE_OR = OR
STATE_PA = PA
STATE_RI = RI
STATE_SC = SC
STATE_SD = SD
STATE_TN = TN
STATE_TX = TX
STATE_UT = UT
STATE_VT = VT
STATE_VA = VA
STATE_WA = WA
STATE_WV = WV
STATE_WI = WI
STATE_WY = WY
TERRITORY_PR = PR
