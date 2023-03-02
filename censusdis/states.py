# Copyright (c) 2022 Darren Erik Vengroff

"""
This module defines state FIPS codes and some utilities for using them.

The US Census identifies states by their
`FIPS Codes <https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code#FIPS_state_codes>`_,
which are two-digit numeric strings. For convenience, we
define identifiers for them.

Each identifier
has a name of the form ``STATE_XX`` where ``XX`` is the two
letter abbreviation for the state. For example, NJ
is the two letter abbreviation for New Jersey, and the
Census state identifier for New Jersey is 34, so::

    import censusdis.states as cds

    state = cds.STATE_NJ

would set the value of `state` to the string `"34"`.
We can use these values in any of the APIs in
`censusdis` that take a state.

There is also a dictionary whose keys are the state
FIPS codes and whose values are strings naming
the states. It is typically used when we want a
more human-friendly name for each state. As in::

    import censusdis.states as cds

    state = cds.STATE_CA

    print(
        f"The name of the state with ID '{state}' "
        f"is '{cds.STATE_NAMES_FROM_IDS[state]}'."
    )

Finally, there is a list of all states. It is often useful
if we want to perform an operation on all states. For
example::

    import censusdis.states as cds

    for state in cds.ALL_STATES:
        do_something_with_a_state(state)

There is also a list that includes all states and the
District of Columbia. It is called ``cds.ALL_STATES_AND_DC``.
"""


STATE_AL = "01"
"""Alabama"""

STATE_AK = "02"
"""Alaska"""

STATE_AZ = "04"
"""Arizona"""

STATE_AR = "05"
"""Arkansas"""

STATE_CA = "06"
"""California"""

STATE_CO = "08"
"""Colorado"""

STATE_CT = "09"
"""Connecticut"""

STATE_DE = "10"
"""Delaware"""

STATE_DC = "11"
"""District of Columbia"""

STATE_FL = "12"
"""Florida"""

STATE_GA = "13"
"""Georgia"""

STATE_HI = "15"
"""Hawaii"""

STATE_ID = "16"
"""Idaho"""

STATE_IL = "17"
"""Illinois"""

STATE_IN = "18"
"""Indiana"""

STATE_IA = "19"
"""Iowa"""

STATE_KS = "20"
"""Kansas"""

STATE_KY = "21"
"""Kentucky"""

STATE_LA = "22"
"""Louisiana"""

STATE_ME = "23"
"""Maine"""

STATE_MD = "24"
"""Maryland"""

STATE_MA = "25"
"""Massachusetts"""

STATE_MI = "26"
"""Michigan"""

STATE_MN = "27"
"""Minnesota"""

STATE_MS = "28"
"""Mississippi"""

STATE_MO = "29"
"""Missouri"""

STATE_MT = "30"
"""Montana"""

STATE_NE = "31"
"""Nebraska"""

STATE_NV = "32"
"""Nevada"""

STATE_NH = "33"
"""New Hampshire"""

STATE_NJ = "34"
"""New Jersey--The Garden State"""

STATE_NM = "35"
"""New Mexico"""

STATE_NY = "36"
"""New York"""

STATE_NC = "37"
"""North Carolina"""

STATE_ND = "38"
"""North Dakota"""

STATE_OH = "39"
"""Ohio"""

STATE_OK = "40"
"""Oklahoma"""

STATE_OR = "41"
"""Oregon"""

STATE_PA = "42"
"""Pennsylvania"""

STATE_RI = "44"
"""Rhode Island"""

STATE_SC = "45"
"""South Carolina"""

STATE_SD = "46"
"""South Dakota"""

STATE_TN = "47"
"""Tennessee"""

STATE_TX = "48"
"""Texas"""

STATE_UT = "49"
"""Utah"""

STATE_VT = "50"
"""Vermont"""

STATE_VA = "51"
"""Virginia"""

STATE_WA = "53"
"""Washington"""

STATE_WV = "54"
"""West Virginia"""

STATE_WI = "55"
"""Wisconsin"""

STATE_WY = "56"
"""Wyoming"""

TERRITORY_PR = "72"
"""Puerto Rico"""


STATE_NAMES_FROM_IDS = {
    STATE_AL: "Alabama",
    STATE_AK: "Alaska",
    STATE_AZ: "Arizona",
    STATE_AR: "Arkansas",
    STATE_CA: "California",
    STATE_CO: "Colorado",
    STATE_CT: "Connecticut",
    STATE_DC: "District of Columbia",
    STATE_DE: "Delaware",
    STATE_FL: "Florida",
    STATE_GA: "Georgia",
    STATE_HI: "Hawaii",
    STATE_ID: "Idaho",
    STATE_IL: "Illinois",
    STATE_IN: "Indiana",
    STATE_IA: "Iowa",
    STATE_KS: "Kansas",
    STATE_KY: "Kentucky",
    STATE_LA: "Louisiana",
    STATE_ME: "Maine",
    STATE_MD: "Maryland",
    STATE_MA: "Massachusetts",
    STATE_MN: "Minnesota",
    STATE_MS: "Mississippi",
    STATE_MI: "Michigan",
    STATE_MO: "Missouri",
    STATE_MT: "Montana",
    STATE_NE: "Nebraska",
    STATE_NV: "Nevada",
    STATE_NH: "New Hampshire",
    STATE_NJ: "New Jersey",
    STATE_NM: "New Mexico",
    STATE_NY: "New York",
    STATE_NC: "North Carolina",
    STATE_ND: "North Dakota",
    STATE_OH: "Ohio",
    STATE_OK: "Oklahoma",
    STATE_OR: "Oregon",
    STATE_PA: "Pennsylvania",
    STATE_RI: "Rhode Island",
    STATE_SC: "South Carolina",
    STATE_SD: "South Dakota",
    STATE_TN: "Tennessee",
    STATE_TX: "Texas",
    STATE_UT: "Utah",
    STATE_VT: "Vermont",
    STATE_VA: "Virginia",
    STATE_WA: "Washington",
    STATE_WV: "West Virginia",
    STATE_WI: "Wisconsin",
    STATE_WY: "Wyoming",
    TERRITORY_PR: "Puerto Rico",
}
"""
The names of each state, indexed by FIPS code.

For example, ``STATE_NAMES_FROM_IDS[STATE_NJ]``
is ``"New Jersey"``.
"""

STATE_ABBREVIATIONS_FROM_IDS = {
    STATE_AL: "AL",
    STATE_AK: "AK",
    STATE_AZ: "AZ",
    STATE_AR: "AR",
    STATE_CA: "CA",
    STATE_CO: "CO",
    STATE_CT: "CT",
    STATE_DC: "DC",
    STATE_DE: "DE",
    STATE_FL: "FL",
    STATE_GA: "GA",
    STATE_HI: "HI",
    STATE_ID: "ID",
    STATE_IL: "IL",
    STATE_IN: "IN",
    STATE_IA: "IA",
    STATE_KS: "KS",
    STATE_KY: "KY",
    STATE_LA: "LA",
    STATE_ME: "ME",
    STATE_MD: "MD",
    STATE_MA: "MA",
    STATE_MN: "MN",
    STATE_MS: "MS",
    STATE_MI: "MI",
    STATE_MO: "MO",
    STATE_MT: "NT",
    STATE_NE: "NE",
    STATE_NV: "NV",
    STATE_NH: "NH",
    STATE_NJ: "NJ",
    STATE_NM: "NM",
    STATE_NY: "NY",
    STATE_NC: "NC",
    STATE_ND: "ND",
    STATE_OH: "OH",
    STATE_OK: "OK",
    STATE_OR: "OR",
    STATE_PA: "PA",
    STATE_RI: "RI",
    STATE_SC: "SC",
    STATE_SD: "SD",
    STATE_TN: "TN",
    STATE_TX: "TX",
    STATE_UT: "UT",
    STATE_VT: "VT",
    STATE_VA: "VA",
    STATE_WA: "WA",
    STATE_WV: "WV",
    STATE_WI: "WI",
    STATE_WY: "WY",
    TERRITORY_PR: "PR",
}
"""
The postal abbreviation of each state, indexed by FIPS code.

For example, ``STATE_NAMES_FROM_IDS[STATE_NJ]``
is ``"NJ"``.
"""

STATE_IDS_FROM_ABBREVIATIONS = {
    v: k for k, v in STATE_ABBREVIATIONS_FROM_IDS.items()
}
"""
The state FIPS code ID for each state abbreviation.

For example ``STATE_IDS_FROM_ABBREVIATIONS['NJ']``
is ``34``, which is the value of``STATE_NJ``.
"""

STATE_IDS_FROM_NAMES = {
    v: k for k, v in STATE_NAMES_FROM_IDS.items()
}
"""
The state FIPS code ID for each state name.

For example ``STATE_IDS_FROM_ABBREVIATIONS['New Jersey']``
is ``34``, which is the value of``STATE_NJ``.
"""

ALL_STATES = [state for state in STATE_NAMES_FROM_IDS if state != STATE_DC]
"""
All the state FIPS codes.

Includes all 50 states, but not DC.

Typically used to iterate over the states, as in::

    from censusdis.states import ALL_STATES

    for state in ALL_STATES:
        process_state(state)
"""

ALL_STATES_DC_AND_PR = list(STATE_NAMES_FROM_IDS.keys())
"""
All the state FIPS codes and DC and PR.

Includes all 50 states, DC and PR.

Typically used to iterate over the states, as in::

    from censusdis.states import ALL_STATES_DC_AND_PR

    for state in ALL_STATES_DC_AND_PR:
        process_state(state)
"""

ALL_STATES_AND_DC = [state for state in ALL_STATES_DC_AND_PR if state != TERRITORY_PR]
"""
All the state FIPS codes and DC.

Includes all 50 states and DC.

Typically used to iterate over the states, as in::

    from censusdis.states import ALL_STATES_AND_DC

    for state in ALL_STATES_AND_DC:
        process_state(state)
"""
