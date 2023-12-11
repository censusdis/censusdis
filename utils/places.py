# Copyright (c) 2023 Darren Erik Vengroff
"""
A utility to generate the symbolic names of all the places.

This should be a one-time thing. But we are retaining this code
here in utils for reference.
"""
from pathlib import Path

import censusdis.data as ced
from censusdis.datasets import ACS5
from censusdis.states import NAMES_FROM_IDS


def drop_suffix(s: str, suffix: str) -> str:
    """Drop a suffix from a string if it is present."""
    if s.endswith(suffix):
        s = s[: -len(suffix)]

    return s


def main():
    """Load names of all places and generate python symbols."""
    # Make sure the target directory is there.
    target_dir = Path(__file__).parent.parent / "censusdis" / "places"

    target_dir.mkdir(exist_ok=True)

    # Load the names.
    df_place_names = ced.download(ACS5, 2022, ["NAME"], state="*", place="*")

    # Test file to import them all.
    test_file = Path(__file__).parent.parent / "tests" / "test_places.py"

    with open(test_file, "w") as tf:
        tf.write(
            """# Copyright (c) 2023 Darren Erik Vengroff
\"\"\"Tests for place symbols.\"\"\"

import unittest


class PlaceTestCase(unittest.TestCase):
    \"\"\"Tests for place symbols.\"\"\"
"""
        )

        for state, df_state in df_place_names.groupby("STATE"):
            state_name = NAMES_FROM_IDS[state]
            state_symbol = state_name.lower().replace(" ", "_")

            print(f"Processing {state_name}/{state_symbol} ({state})")

            tf.write(
                f"""
    def test_{state_symbol}(self):
        \"\"\"Test {state_name}.\"\"\"
        import censusdis.places.{state_symbol}

        symbols = [
            symbol
            for symbol, val in censusdis.places.{state_symbol}.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual({len(df_state.index)}, sym_count)
"""
            )

            state_file = target_dir / f"{state_symbol}.py"

            with open(state_file, "w") as sf:
                sf.writelines(
                    [
                        "# Copyright (c) 2023 Darren Erik Vengroff\n",
                        f'"""Places in {state_name}."""\n',
                        "\n",
                        "\n",
                    ]
                )
                for _, row in df_state.sort_values(by="NAME").iterrows():
                    place = row["PLACE"]

                    symbol = row["NAME"]
                    symbol = symbol.split(", ")[0]
                    symbol = symbol.upper()

                    symbol = symbol.replace(" ", "_")
                    symbol = symbol.replace("-", "_")
                    symbol = symbol.replace("/", "_")
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

                    sf.write(f'{symbol} = "{place}"\n')


if __name__ == "__main__":
    main()
