# Copyright (c) 2022 Darren Erik Vengroff

"""
State identifiers.

The first set of identifiers are the numeric strings
used by the US Census to identify states. Each one
has a name of the form `STATE_XX` where `XX` is the two
letter abbreviation for the state. For example, NJ
is the two letter abbreviation for New Jersey, and the
Census state identifier for New Jersey is 34, so::

    import censusdis.states as cds

    state = cds.STATE_NJ

would set the value of `state` to the string `"34"`.
We can use these values in any of the APIs in
`censusdis` that take a state.

The second set of identifiers use these state IDs as
keys in a dictionary whose values are strings naming
the states. These are stored in a dictionary that
we can use for printing state names. For example::

    import censusdis.states as cds

    state = cds.STATE_CA

    print(
        f"The name of the state with ID {state} "
        f"is {cds.STATE_NAMES_FROM_IDS[state]."
    )

Finally, there is a list of all states. It is often useful
if we want to perform an operation on all states. For
example::

    import censusdis.states as cds

    for state in cds.ALL_STATES:
        do_something_with_a_state(state)

There is also a list that includes all states and the
District of Columbig. It is called `cds.ALL_STATES_AND_DC`.
"""

# State and county IDs we are interested in:
STATE_AL = "01"
STATE_AK = "02"
STATE_AZ = "04"
STATE_AR = "05"
STATE_CA = "06"
STATE_CO = "08"
STATE_CT = "09"
STATE_DE = "10"
STATE_DC = "11"
STATE_FL = "12"
STATE_GA = "13"
STATE_HI = "15"
STATE_ID = "16"
STATE_IL = "17"
STATE_IN = "18"
STATE_IA = "19"
STATE_KS = "20"
STATE_KY = "21"
STATE_LA = "22"
STATE_ME = "23"
STATE_MD = "24"
STATE_MA = "25"
STATE_MI = "26"
STATE_MN = "27"
STATE_MS = "28"
STATE_MO = "29"
STATE_MT = "30"
STATE_NE = "31"
STATE_NV = "32"
STATE_NH = "33"
STATE_NJ = "34"
STATE_NM = "35"
STATE_NY = "36"
STATE_NC = "37"
STATE_ND = "38"
STATE_OH = "39"
STATE_OK = "40"
STATE_OR = "41"
STATE_PA = "42"
STATE_RI = "44"
STATE_SC = "45"
STATE_SD = "46"
STATE_TN = "47"
STATE_TX = "48"
STATE_UT = "49"
STATE_VT = "50"
STATE_VA = "51"
STATE_WA = "53"
STATE_WV = "54"
STATE_WI = "55"
STATE_WY = "56"

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
}

ALL_STATES = [state for state in STATE_NAMES_FROM_IDS if state != STATE_DC]

ALL_STATES_AND_DC = list(STATE_NAMES_FROM_IDS.keys())
