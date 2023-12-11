# Copyright (c) 2023 Darren Erik Vengroff
"""
A utility to generate the symbolic names of a variety of top-level geos.

This should be a one-time thing. But we are retaining this code
here in utils for reference.
"""
from pathlib import Path

import censusdis.data as ced
from censusdis.datasets import ACS5


def drop_suffix(s: str, suffix: str) -> str:
    """Drop a suffix from a string if it is present."""
    if s.endswith(suffix):
        s = s[: -len(suffix)]

    return s


def main():
    """Load names of all places and generate python symbols."""
    for geo, short_geo in [
        ("metropolitan_statistical_area_micropolitan_statistical_area", "msa_msa"),
        ("combined_statistical_area", "csa"),
        ("region", "region"),
        ("division", "division"),
    ]:
        generate_for_geo(geo, short_geo)


def generate_for_geo(geo: str, short_geo: str):
    """Generate symbols and tests for a geography."""
    # Load the names.
    geo_dict = {geo: "*"}

    df_geos = ced.download(ACS5, 2022, ["NAME"], **geo_dict)

    target_dir = Path(__file__).parent.parent / "censusdis"

    # Test file to import them all.
    test_file = Path(__file__).parent.parent / "tests" / f"test_{short_geo}.py"
    with open(test_file, "w") as tf:
        tf.write(
            f"""# Copyright (c) 2023 Darren Erik Vengroff
\"\"\"Tests for {geo.replace('_', ' ').title()} symbols.\"\"\"

import unittest

import censusdis.{short_geo}


class {short_geo.title()}TestCase(unittest.TestCase):
    \"\"\"Tests for {geo.replace('_', ' ').title()} symbols.\"\"\"
    
    def test_{geo}s(self):
        \"\"\"Test {geo}.\"\"\"
        symbols = [
            symbol
            for symbol, val in censusdis.{short_geo}.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual({len(df_geos.index)}, sym_count)
"""
        )

        geo_file = target_dir / f"{short_geo}.py"

        with open(geo_file, "w") as sf:
            sf.writelines(
                [
                    "# Copyright (c) 2023 Darren Erik Vengroff\n",
                    f'"""{geo.replace("_", " ").title()}s."""\n',
                    "\n",
                    "\n",
                ]
            )
            for _, row in df_geos.sort_values(by="NAME").iterrows():
                geo_value = row[f"{geo.upper()}"]

                symbol = row["NAME"]
                symbol = symbol.upper()

                symbol = symbol.replace(", ", "_")
                symbol = symbol.replace(" ", "_")
                symbol = symbol.replace("-", "_")
                symbol = symbol.replace("/", "_")

                symbol = symbol.replace("__", "_")

                symbol = symbol.replace("'", "")
                symbol = symbol.replace(".", "")
                symbol = symbol.replace("(", "")
                symbol = symbol.replace(")", "")

                # For PR in case of non UTF8 source code.
                symbol = symbol.replace("Á", "A")
                symbol = symbol.replace("Í", "I")
                symbol = symbol.replace("Ñ", "N")
                symbol = symbol.replace("Ó", "O")
                symbol = symbol.replace("Ü", "U")

                sf.write(f'{symbol} = "{geo_value}"\n')


if __name__ == "__main__":
    main()
