# Copyright (c) 2023 Darren Erik Vengroff
"""
Counties in Connecticut.

Connecticut is a little different than other states because in 2022,
the U.S. Census, at the state's request, began tracking planning
regions as county-like divisions.

We support both symbolically. Which one you get back from the census for
county queries will depend on the data set and vintage.

See
https://www.federalregister.gov/documents/2022/06/06/2022-12063/change-to-county-equivalents-in-the-state-of-connecticut
for more on this.
"""

# Pre-2022 counties.
FAIRFIELD = "001"
HARTFORD = "003"
LITCHFIELD = "005"
MIDDLESEX = "007"
NEW_HAVEN = "009"
NEW_LONDON = "011"
TOLLAND = "013"
WINDHAM = "015"

# Post-2020 planning regions.
CAPITOL_PLANNING_REGION = "110"
GREATER_BRIDGEPORT_PLANNING_REGION = "120"
LOWER_CONNECTICUT_RIVER_VALLEY_PLANNING_REGION = "130"
NAUGATUCK_VALLEY_PLANNING_REGION = "140"
NORTHEASTERN_CONNECTICUT_PLANNING_REGION = "150"
NORTHWEST_HILLS_PLANNING_REGION = "160"
SOUTH_CENTRAL_CONNECTICUT_PLANNING_REGION = "170"
SOUTHEASTERN_CONNECTICUT_PLANNING_REGION = "180"
WESTERN_CONNECTICUT_PLANNING_REGION = "190"
