# Copyright (c) 2023 Darren Erik Vengroff
"""Tests for county symbols."""

import unittest


class CountyTestCase(unittest.TestCase):
    """Tests for county symbols."""

    def test_alabama(self):
        """Test Alabama."""
        import censusdis.counties.alabama

        symbols = [
            symbol
            for symbol, val in censusdis.counties.alabama.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(67, sym_count)

    def test_alaska(self):
        """Test Alaska."""
        import censusdis.counties.alaska

        symbols = [
            symbol
            for symbol, val in censusdis.counties.alaska.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(30, sym_count)

    def test_arizona(self):
        """Test Arizona."""
        import censusdis.counties.arizona

        symbols = [
            symbol
            for symbol, val in censusdis.counties.arizona.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(15, sym_count)

    def test_arkansas(self):
        """Test Arkansas."""
        import censusdis.counties.arkansas

        symbols = [
            symbol
            for symbol, val in censusdis.counties.arkansas.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(75, sym_count)

    def test_california(self):
        """Test California."""
        import censusdis.counties.california

        symbols = [
            symbol
            for symbol, val in censusdis.counties.california.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(58, sym_count)

    def test_colorado(self):
        """Test Colorado."""
        import censusdis.counties.colorado

        symbols = [
            symbol
            for symbol, val in censusdis.counties.colorado.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(64, sym_count)

    def test_connecticut(self):
        """Test Connecticut."""
        import censusdis.counties.connecticut

        symbols = [
            symbol
            for symbol, val in censusdis.counties.connecticut.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(17, sym_count)

    def test_delaware(self):
        """Test Delaware."""
        import censusdis.counties.delaware

        symbols = [
            symbol
            for symbol, val in censusdis.counties.delaware.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(3, sym_count)

    def test_district_of_columbia(self):
        """Test District of Columbia."""
        import censusdis.counties.district_of_columbia

        symbols = [
            symbol
            for symbol, val in censusdis.counties.district_of_columbia.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(1, sym_count)

    def test_florida(self):
        """Test Florida."""
        import censusdis.counties.florida

        symbols = [
            symbol
            for symbol, val in censusdis.counties.florida.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(67, sym_count)

    def test_georgia(self):
        """Test Georgia."""
        import censusdis.counties.georgia

        symbols = [
            symbol
            for symbol, val in censusdis.counties.georgia.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(159, sym_count)

    def test_hawaii(self):
        """Test Hawaii."""
        import censusdis.counties.hawaii

        symbols = [
            symbol
            for symbol, val in censusdis.counties.hawaii.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(5, sym_count)

    def test_idaho(self):
        """Test Idaho."""
        import censusdis.counties.idaho

        symbols = [
            symbol
            for symbol, val in censusdis.counties.idaho.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(44, sym_count)

    def test_illinois(self):
        """Test Illinois."""
        import censusdis.counties.illinois

        symbols = [
            symbol
            for symbol, val in censusdis.counties.illinois.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(102, sym_count)

    def test_indiana(self):
        """Test Indiana."""
        import censusdis.counties.indiana

        symbols = [
            symbol
            for symbol, val in censusdis.counties.indiana.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(92, sym_count)

    def test_iowa(self):
        """Test Iowa."""
        import censusdis.counties.iowa

        symbols = [
            symbol
            for symbol, val in censusdis.counties.iowa.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(99, sym_count)

    def test_kansas(self):
        """Test Kansas."""
        import censusdis.counties.kansas

        symbols = [
            symbol
            for symbol, val in censusdis.counties.kansas.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(105, sym_count)

    def test_kentucky(self):
        """Test Kentucky."""
        import censusdis.counties.kentucky

        symbols = [
            symbol
            for symbol, val in censusdis.counties.kentucky.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(120, sym_count)

    def test_louisiana(self):
        """Test Louisiana."""
        import censusdis.counties.louisiana

        symbols = [
            symbol
            for symbol, val in censusdis.counties.louisiana.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(64, sym_count)

    def test_maine(self):
        """Test Maine."""
        import censusdis.counties.maine

        symbols = [
            symbol
            for symbol, val in censusdis.counties.maine.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(16, sym_count)

    def test_maryland(self):
        """Test Maryland."""
        import censusdis.counties.maryland

        symbols = [
            symbol
            for symbol, val in censusdis.counties.maryland.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(24, sym_count)

    def test_massachusetts(self):
        """Test Massachusetts."""
        import censusdis.counties.massachusetts

        symbols = [
            symbol
            for symbol, val in censusdis.counties.massachusetts.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(14, sym_count)

    def test_michigan(self):
        """Test Michigan."""
        import censusdis.counties.michigan

        symbols = [
            symbol
            for symbol, val in censusdis.counties.michigan.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(83, sym_count)

    def test_minnesota(self):
        """Test Minnesota."""
        import censusdis.counties.minnesota

        symbols = [
            symbol
            for symbol, val in censusdis.counties.minnesota.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(87, sym_count)

    def test_mississippi(self):
        """Test Mississippi."""
        import censusdis.counties.mississippi

        symbols = [
            symbol
            for symbol, val in censusdis.counties.mississippi.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(82, sym_count)

    def test_missouri(self):
        """Test Missouri."""
        import censusdis.counties.missouri

        symbols = [
            symbol
            for symbol, val in censusdis.counties.missouri.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(115, sym_count)

    def test_montana(self):
        """Test Montana."""
        import censusdis.counties.montana

        symbols = [
            symbol
            for symbol, val in censusdis.counties.montana.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(56, sym_count)

    def test_nebraska(self):
        """Test Nebraska."""
        import censusdis.counties.nebraska

        symbols = [
            symbol
            for symbol, val in censusdis.counties.nebraska.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(93, sym_count)

    def test_nevada(self):
        """Test Nevada."""
        import censusdis.counties.nevada

        symbols = [
            symbol
            for symbol, val in censusdis.counties.nevada.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(17, sym_count)

    def test_new_hampshire(self):
        """Test New Hampshire."""
        import censusdis.counties.new_hampshire

        symbols = [
            symbol
            for symbol, val in censusdis.counties.new_hampshire.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(10, sym_count)

    def test_new_jersey(self):
        """Test New Jersey."""
        import censusdis.counties.new_jersey

        symbols = [
            symbol
            for symbol, val in censusdis.counties.new_jersey.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(21, sym_count)

    def test_new_mexico(self):
        """Test New Mexico."""
        import censusdis.counties.new_mexico

        symbols = [
            symbol
            for symbol, val in censusdis.counties.new_mexico.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(33, sym_count)

    def test_new_york(self):
        """Test New York."""
        import censusdis.counties.new_york

        symbols = [
            symbol
            for symbol, val in censusdis.counties.new_york.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(62, sym_count)

    def test_north_carolina(self):
        """Test North Carolina."""
        import censusdis.counties.north_carolina

        symbols = [
            symbol
            for symbol, val in censusdis.counties.north_carolina.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(100, sym_count)

    def test_north_dakota(self):
        """Test North Dakota."""
        import censusdis.counties.north_dakota

        symbols = [
            symbol
            for symbol, val in censusdis.counties.north_dakota.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(53, sym_count)

    def test_ohio(self):
        """Test Ohio."""
        import censusdis.counties.ohio

        symbols = [
            symbol
            for symbol, val in censusdis.counties.ohio.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(88, sym_count)

    def test_oklahoma(self):
        """Test Oklahoma."""
        import censusdis.counties.oklahoma

        symbols = [
            symbol
            for symbol, val in censusdis.counties.oklahoma.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(77, sym_count)

    def test_oregon(self):
        """Test Oregon."""
        import censusdis.counties.oregon

        symbols = [
            symbol
            for symbol, val in censusdis.counties.oregon.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(36, sym_count)

    def test_pennsylvania(self):
        """Test Pennsylvania."""
        import censusdis.counties.pennsylvania

        symbols = [
            symbol
            for symbol, val in censusdis.counties.pennsylvania.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(67, sym_count)

    def test_rhode_island(self):
        """Test Rhode Island."""
        import censusdis.counties.rhode_island

        symbols = [
            symbol
            for symbol, val in censusdis.counties.rhode_island.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(5, sym_count)

    def test_south_carolina(self):
        """Test South Carolina."""
        import censusdis.counties.south_carolina

        symbols = [
            symbol
            for symbol, val in censusdis.counties.south_carolina.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(46, sym_count)

    def test_south_dakota(self):
        """Test South Dakota."""
        import censusdis.counties.south_dakota

        symbols = [
            symbol
            for symbol, val in censusdis.counties.south_dakota.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(66, sym_count)

    def test_tennessee(self):
        """Test Tennessee."""
        import censusdis.counties.tennessee

        symbols = [
            symbol
            for symbol, val in censusdis.counties.tennessee.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(95, sym_count)

    def test_texas(self):
        """Test Texas."""
        import censusdis.counties.texas

        symbols = [
            symbol
            for symbol, val in censusdis.counties.texas.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(254, sym_count)

    def test_utah(self):
        """Test Utah."""
        import censusdis.counties.utah

        symbols = [
            symbol
            for symbol, val in censusdis.counties.utah.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(29, sym_count)

    def test_vermont(self):
        """Test Vermont."""
        import censusdis.counties.vermont

        symbols = [
            symbol
            for symbol, val in censusdis.counties.vermont.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(14, sym_count)

    def test_virginia(self):
        """Test Virginia."""
        import censusdis.counties.virginia

        symbols = [
            symbol
            for symbol, val in censusdis.counties.virginia.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(133, sym_count)

    def test_washington(self):
        """Test Washington."""
        import censusdis.counties.washington

        symbols = [
            symbol
            for symbol, val in censusdis.counties.washington.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(39, sym_count)

    def test_west_virginia(self):
        """Test West Virginia."""
        import censusdis.counties.west_virginia

        symbols = [
            symbol
            for symbol, val in censusdis.counties.west_virginia.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(55, sym_count)

    def test_wisconsin(self):
        """Test Wisconsin."""
        import censusdis.counties.wisconsin

        symbols = [
            symbol
            for symbol, val in censusdis.counties.wisconsin.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(72, sym_count)

    def test_wyoming(self):
        """Test Wyoming."""
        import censusdis.counties.wyoming

        symbols = [
            symbol
            for symbol, val in censusdis.counties.wyoming.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(23, sym_count)

    def test_puerto_rico(self):
        """Test Puerto Rico."""
        import censusdis.counties.puerto_rico

        symbols = [
            symbol
            for symbol, val in censusdis.counties.puerto_rico.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(78, sym_count)
