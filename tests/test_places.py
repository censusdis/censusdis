# Copyright (c) 2023 Darren Erik Vengroff
"""Tests for place symbols."""

import unittest


class PlaceTestCase(unittest.TestCase):
    """Tests for place symbols."""

    def test_alabama(self):
        """Test Alabama."""
        import censusdis.places.alabama

        symbols = [
            symbol
            for symbol, val in censusdis.places.alabama.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(593, sym_count)

    def test_alaska(self):
        """Test Alaska."""
        import censusdis.places.alaska

        symbols = [
            symbol
            for symbol, val in censusdis.places.alaska.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(355, sym_count)

    def test_arizona(self):
        """Test Arizona."""
        import censusdis.places.arizona

        symbols = [
            symbol
            for symbol, val in censusdis.places.arizona.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(467, sym_count)

    def test_arkansas(self):
        """Test Arkansas."""
        import censusdis.places.arkansas

        symbols = [
            symbol
            for symbol, val in censusdis.places.arkansas.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(625, sym_count)

    def test_california(self):
        """Test California."""
        import censusdis.places.california

        symbols = [
            symbol
            for symbol, val in censusdis.places.california.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1611, sym_count)

    def test_colorado(self):
        """Test Colorado."""
        import censusdis.places.colorado

        symbols = [
            symbol
            for symbol, val in censusdis.places.colorado.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(482, sym_count)

    def test_connecticut(self):
        """Test Connecticut."""
        import censusdis.places.connecticut

        symbols = [
            symbol
            for symbol, val in censusdis.places.connecticut.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(215, sym_count)

    def test_delaware(self):
        """Test Delaware."""
        import censusdis.places.delaware

        symbols = [
            symbol
            for symbol, val in censusdis.places.delaware.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(79, sym_count)

    def test_district_of_columbia(self):
        """Test District of Columbia."""
        import censusdis.places.district_of_columbia

        symbols = [
            symbol
            for symbol, val in censusdis.places.district_of_columbia.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1, sym_count)

    def test_florida(self):
        """Test Florida."""
        import censusdis.places.florida

        symbols = [
            symbol
            for symbol, val in censusdis.places.florida.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(955, sym_count)

    def test_georgia(self):
        """Test Georgia."""
        import censusdis.places.georgia

        symbols = [
            symbol
            for symbol, val in censusdis.places.georgia.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(675, sym_count)

    def test_hawaii(self):
        """Test Hawaii."""
        import censusdis.places.hawaii

        symbols = [
            symbol
            for symbol, val in censusdis.places.hawaii.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(163, sym_count)

    def test_idaho(self):
        """Test Idaho."""
        import censusdis.places.idaho

        symbols = [
            symbol
            for symbol, val in censusdis.places.idaho.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(237, sym_count)

    def test_illinois(self):
        """Test Illinois."""
        import censusdis.places.illinois

        symbols = [
            symbol
            for symbol, val in censusdis.places.illinois.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1464, sym_count)

    def test_indiana(self):
        """Test Indiana."""
        import censusdis.places.indiana

        symbols = [
            symbol
            for symbol, val in censusdis.places.indiana.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(973, sym_count)

    def test_iowa(self):
        """Test Iowa."""
        import censusdis.places.iowa

        symbols = [
            symbol
            for symbol, val in censusdis.places.iowa.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1027, sym_count)

    def test_kansas(self):
        """Test Kansas."""
        import censusdis.places.kansas

        symbols = [
            symbol
            for symbol, val in censusdis.places.kansas.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(740, sym_count)

    def test_kentucky(self):
        """Test Kentucky."""
        import censusdis.places.kentucky

        symbols = [
            symbol
            for symbol, val in censusdis.places.kentucky.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(554, sym_count)

    def test_louisiana(self):
        """Test Louisiana."""
        import censusdis.places.louisiana

        symbols = [
            symbol
            for symbol, val in censusdis.places.louisiana.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(488, sym_count)

    def test_maine(self):
        """Test Maine."""
        import censusdis.places.maine

        symbols = [
            symbol
            for symbol, val in censusdis.places.maine.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(155, sym_count)

    def test_maryland(self):
        """Test Maryland."""
        import censusdis.places.maryland

        symbols = [
            symbol
            for symbol, val in censusdis.places.maryland.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(536, sym_count)

    def test_massachusetts(self):
        """Test Massachusetts."""
        import censusdis.places.massachusetts

        symbols = [
            symbol
            for symbol, val in censusdis.places.massachusetts.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(248, sym_count)

    def test_michigan(self):
        """Test Michigan."""
        import censusdis.places.michigan

        symbols = [
            symbol
            for symbol, val in censusdis.places.michigan.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(745, sym_count)

    def test_minnesota(self):
        """Test Minnesota."""
        import censusdis.places.minnesota

        symbols = [
            symbol
            for symbol, val in censusdis.places.minnesota.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(914, sym_count)

    def test_mississippi(self):
        """Test Mississippi."""
        import censusdis.places.mississippi

        symbols = [
            symbol
            for symbol, val in censusdis.places.mississippi.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(427, sym_count)

    def test_missouri(self):
        """Test Missouri."""
        import censusdis.places.missouri

        symbols = [
            symbol
            for symbol, val in censusdis.places.missouri.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1082, sym_count)

    def test_montana(self):
        """Test Montana."""
        import censusdis.places.montana

        symbols = [
            symbol
            for symbol, val in censusdis.places.montana.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(497, sym_count)

    def test_nebraska(self):
        """Test Nebraska."""
        import censusdis.places.nebraska

        symbols = [
            symbol
            for symbol, val in censusdis.places.nebraska.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(590, sym_count)

    def test_nevada(self):
        """Test Nevada."""
        import censusdis.places.nevada

        symbols = [
            symbol
            for symbol, val in censusdis.places.nevada.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(133, sym_count)

    def test_new_hampshire(self):
        """Test New Hampshire."""
        import censusdis.places.new_hampshire

        symbols = [
            symbol
            for symbol, val in censusdis.places.new_hampshire.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(100, sym_count)

    def test_new_jersey(self):
        """Test New Jersey."""
        import censusdis.places.new_jersey

        symbols = [
            symbol
            for symbol, val in censusdis.places.new_jersey.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(700, sym_count)

    def test_new_mexico(self):
        """Test New Mexico."""
        import censusdis.places.new_mexico

        symbols = [
            symbol
            for symbol, val in censusdis.places.new_mexico.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(527, sym_count)

    def test_new_york(self):
        """Test New York."""
        import censusdis.places.new_york

        symbols = [
            symbol
            for symbol, val in censusdis.places.new_york.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1293, sym_count)

    def test_north_carolina(self):
        """Test North Carolina."""
        import censusdis.places.north_carolina

        symbols = [
            symbol
            for symbol, val in censusdis.places.north_carolina.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(776, sym_count)

    def test_north_dakota(self):
        """Test North Dakota."""
        import censusdis.places.north_dakota

        symbols = [
            symbol
            for symbol, val in censusdis.places.north_dakota.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(406, sym_count)

    def test_ohio(self):
        """Test Ohio."""
        import censusdis.places.ohio

        symbols = [
            symbol
            for symbol, val in censusdis.places.ohio.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1265, sym_count)

    def test_oklahoma(self):
        """Test Oklahoma."""
        import censusdis.places.oklahoma

        symbols = [
            symbol
            for symbol, val in censusdis.places.oklahoma.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(845, sym_count)

    def test_oregon(self):
        """Test Oregon."""
        import censusdis.places.oregon

        symbols = [
            symbol
            for symbol, val in censusdis.places.oregon.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(426, sym_count)

    def test_pennsylvania(self):
        """Test Pennsylvania."""
        import censusdis.places.pennsylvania

        symbols = [
            symbol
            for symbol, val in censusdis.places.pennsylvania.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1888, sym_count)

    def test_rhode_island(self):
        """Test Rhode Island."""
        import censusdis.places.rhode_island

        symbols = [
            symbol
            for symbol, val in censusdis.places.rhode_island.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(36, sym_count)

    def test_south_carolina(self):
        """Test South Carolina."""
        import censusdis.places.south_carolina

        symbols = [
            symbol
            for symbol, val in censusdis.places.south_carolina.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(475, sym_count)

    def test_south_dakota(self):
        """Test South Dakota."""
        import censusdis.places.south_dakota

        symbols = [
            symbol
            for symbol, val in censusdis.places.south_dakota.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(486, sym_count)

    def test_tennessee(self):
        """Test Tennessee."""
        import censusdis.places.tennessee

        symbols = [
            symbol
            for symbol, val in censusdis.places.tennessee.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(504, sym_count)

    def test_texas(self):
        """Test Texas."""
        import censusdis.places.texas

        symbols = [
            symbol
            for symbol, val in censusdis.places.texas.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1862, sym_count)

    def test_utah(self):
        """Test Utah."""
        import censusdis.places.utah

        symbols = [
            symbol
            for symbol, val in censusdis.places.utah.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(333, sym_count)

    def test_vermont(self):
        """Test Vermont."""
        import censusdis.places.vermont

        symbols = [
            symbol
            for symbol, val in censusdis.places.vermont.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(179, sym_count)

    def test_virginia(self):
        """Test Virginia."""
        import censusdis.places.virginia

        symbols = [
            symbol
            for symbol, val in censusdis.places.virginia.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(672, sym_count)

    def test_washington(self):
        """Test Washington."""
        import censusdis.places.washington

        symbols = [
            symbol
            for symbol, val in censusdis.places.washington.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(639, sym_count)

    def test_west_virginia(self):
        """Test West Virginia."""
        import censusdis.places.west_virginia

        symbols = [
            symbol
            for symbol, val in censusdis.places.west_virginia.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(439, sym_count)

    def test_wisconsin(self):
        """Test Wisconsin."""
        import censusdis.places.wisconsin

        symbols = [
            symbol
            for symbol, val in censusdis.places.wisconsin.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(807, sym_count)

    def test_wyoming(self):
        """Test Wyoming."""
        import censusdis.places.wyoming

        symbols = [
            symbol
            for symbol, val in censusdis.places.wyoming.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(205, sym_count)

    def test_puerto_rico(self):
        """Test Puerto Rico."""
        import censusdis.places.puerto_rico

        symbols = [
            symbol
            for symbol, val in censusdis.places.puerto_rico.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(292, sym_count)
