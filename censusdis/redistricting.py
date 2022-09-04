import censusdata
import pandas as pd
from typing import List, Optional
import requests


_DEFAULT_DEC_PL_CENSUS_FIELDS = [
    'P1_001N', 'P1_003N', 'P1_004N',
]

# Different group names were used in 2000.
_2000_GROUP_NAMES = {
    'P1': 'PL001',
    'P2': 'PL002',
}


def field_map(year: int, group: str = 'P2'):
    # Unfortunately 'dec/pl' is not accepted by
    # censusdata.censustable, so we have to do things
    # a little more manually.
    #
    # metadata = censusdata.censustable('dec/pl', year, 'P1')

    if year == 2000:
        group = _2000_GROUP_NAMES[group]

    request = requests.get('https://api.census.gov/data/{:04d}/dec/pl/groups/{:}/'.format(year, group))
    metadata = request.json()

    fields = {}
    black_fields = []
    white_fields = []
    asian_fields = []
    native_american_fields = []
    hawaiian_fields = []

    hispanic_latino_fields = []

    black_alone_fields = []
    white_alone_fields = []
    asian_alone_fields = []
    native_american_alone_fields = []
    hawaiian_alone_fields = []

    two_or_more_races = []

    total_field = ''

    # The rules here embed knowledge of the naming
    # schemes used in 2010 and 2020, which differ.
    for k, v in metadata['variables'].items():
        if not k.endswith('ERR'):
            if (k.endswith('001') or k.endswith('001N')) and ('Total' in v['label']):
                total_field = k
            if v['label'] != 'Total':
                if not v['label'].startswith('Annotation'):
                    components = v['label'].split('!!')

                    if not components[-1].endswith('race'):
                        if components[-1] != 'Not Hispanic or Latino':
                            if 'two or more races' in components[-1].lower():
                                fields[k] = components[-1]
                                two_or_more_races.append(k)
                            elif not components[-1].endswith('races'):
                                if not components[-1].endswith(':'):
                                    fields[k] = components[-1]
                                    if 'Black' in components[-1] or 'black' in components[-1]:
                                        black_fields.append(k)
                                        if 'alone' in components[-1]:
                                            black_alone_fields.append(k)

                                    if 'White' in components[-1] or 'white' in components[-1]:
                                        white_fields.append(k)
                                        if 'alone' in components[-1]:
                                            white_alone_fields.append(k)

                                    if 'Asian' in components[-1] or 'asian' in components[-1]:
                                        asian_fields.append(k)
                                        if 'alone' in components[-1]:
                                            asian_alone_fields.append(k)

                                    if 'Native' in components[-1] or 'native' in components[-1]:
                                        if 'Alaska' in components[-1] or 'alaska' in components[-1]:
                                            native_american_fields.append(k)
                                            if 'alone' in components[-1]:
                                                native_american_alone_fields.append(k)
                                        elif 'Hawaiian' in components[-1] or 'hawaiian' in components[-1]:
                                            hawaiian_fields.append(k)
                                            if 'alone' in components[-1]:
                                                hawaiian_alone_fields.append(k)

                                    if 'Hispanic or Latino' in components[-1]:
                                        hispanic_latino_fields.append(k)

    return {
        'all': fields,
        'total': total_field,
        'black': black_fields,
        'white': white_fields,
        "asian": asian_fields,
        "american_indian_and_alaska_native": native_american_fields,
        "native_hawaiian_and_other_pacific_islander": hawaiian_fields,

        "hispanic_or_latino": hispanic_latino_fields,

        'black_alone': black_alone_fields,
        'white_alone': white_alone_fields,
        'asian_alone': asian_alone_fields,
        'american_indian_and_alaska_native_alone': native_american_alone_fields,
        "native_hawaiian_and_other_pacific_islander_alone": hawaiian_alone_fields,

        'two_or_more_races': two_or_more_races
    }


def geo_state(geo):
    d = dict(geo.params())
    return d['state']


def geo_county(geo):
    d = dict(geo.params())
    return d['county']


def geo_cousub(geo):
    d = dict(geo.params())
    return d['county subdivision']


def geo_tract(geo):
    d = dict(geo.params())
    return d['tract']


def geo_block_group(geo):
    d = dict(geo.params())
    return d['block group']


def geo_block(geo):
    d = dict(geo.params())
    return d['block']


def census_redistricting_data(
        states: str,
        year: int,
        county: Optional[str] = None,
        tract: Optional[str] = None,
        cousub: Optional[str] = None,
        block_group: Optional[str] = None,
        block: Optional[str] = None,
        census_fields: Optional[List[str]] = None,
) -> pd.DataFrame:

    if census_fields is None:
        census_fields = _DEFAULT_DEC_PL_CENSUS_FIELDS

    geo = [
        ('state', states),
    ]

    if county is not None:
        geo.append(('county', county))
    if cousub is not None:
        geo.append(('county subdivision', cousub))
    if tract is not None:
        geo.append(('tract', tract))
    if block_group is not None:
        geo.append(('block group', block_group))
    if block is not None:
        geo.append(('block', block))

    df = censusdata.download(
        'dec/pl', year,
        censusdata.censusgeo(geo),
        census_fields,
    )

    df['STATE'] = df.index.map(geo_state)

    if county is not None:
        df['COUNTY'] = df.index.map(geo_county)
    if cousub is not None:
        df['COUSUB'] = df.index.map(geo_cousub)
    if tract is not None:
        df['TRACT'] = df.index.map(geo_tract)
    if block_group is not None:
        df['BLOCK_GROUP'] = df.index.map(geo_block_group)
    if block is not None:
        df['BLOCK'] = df.index.map(geo_block)

    df.reset_index(inplace=True, drop=True)

    return df


def census_voting_field_metadata(
        census_field: str,
        year: int
):
    baseurl = 'https://api.census.gov/data'

    url = f"{baseurl}/{year}/cps/voting/nov/variables/{census_field}.json"

    r = requests.get(url)

    if r.status_code != 200:
        raise ValueError(f"{r.url} returned status code {r.status_code} and body:\n{r.text}")

    metadata = r.json()

    return metadata


def census_voting_data(
        states: str,
        year: int,
        census_fields: List[str],
        weight_field: str = 'PWSSWGT'
):
    baseurl = 'https://api.census.gov/data'

    url = f"{baseurl}/{year}/cps/voting/nov?tabulate=weight({weight_field})&row+for&row+" \
          f"{'&row+'.join(census_fields)}&for=state:{states}"

    r = requests.get(url)

    if r.status_code != 200:
        raise ValueError(f"{r.url} returned status code {r.status_code} and body:\n{r.text}")

    data = r.json()

    field_values = {}

    for field in census_fields:
        metadata = census_voting_field_metadata(field, year)
        field_values[field] = metadata['values']['item']

    columns = data[0]
    values = [
        [field_values.get(column, {}).get(val, val) for column, val in zip(columns, row)]
        for row in data[1:]
    ]

    df = pd.DataFrame(values, columns=columns)

    return df
