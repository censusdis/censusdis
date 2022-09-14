from typing import Iterable, Optional


class CanonicalGeography:

    # We hide this object inside the class to make __init__
    # effectively private. If you don't have access to this
    # key you can't successfully call __init___.
    __init_key = object()

    def __init__(self, path: Iterable[str], init_key: Optional = None):
        if init_key is not CanonicalGeography.__init_key:
            raise ValueError(
                "CanonicalGeographies cannot be created directly. "
                "Try `CanonicalGeography.partial_matches(**kwargs)` or "
                "`CanonicalGeography.full_match(**kwargs) instead."
            )

        self._path = list(path)

    def __str__(self):
        return ":".join(self._path)

    def __len__(self):
        return len(self._path)

    @property
    def path(self):
        return self._path

    @staticmethod
    def _u2s(**kwargs):
        return {k.replace("_", " "): v for k, v in kwargs.items()}

    def _partial_match(self, is_prefix=True, **kwargs):
        kwargs = self._u2s(**kwargs)
        path_elements_in_kwargs = [k for k in self._path if k in kwargs]
        keys_from_kwargs = [k for k in kwargs.keys()]

        match = path_elements_in_kwargs and (
            path_elements_in_kwargs == keys_from_kwargs
        )

        if is_prefix:
            return match and path_elements_in_kwargs[0] == self._path[0]

        return match

    def _full_match(self, **kwargs):
        return self._partial_match(**kwargs) and len(kwargs) == len(self._path)

    def fill_in(self, **kwargs):
        if not self._partial_match(**kwargs):
            raise ValueError("Must be at least a partial match to fill in.")
        reversed_result = {}
        matching = False
        kwargs = self._u2s(**kwargs)

        for element in reversed(self._path):
            matching = matching or element in kwargs.keys()
            if matching:
                reversed_result[element] = kwargs.get(element, "*")

        result = {k: reversed_result[k] for k in reversed(reversed_result.keys())}

        return result

    def keys(self):
        return list(self._path)

    @classmethod
    def partial_matches(cls, is_prefix=True, **kwargs):
        return {
            num: cg
            for num, cg in cls.ALL.items()
            if cg._partial_match(is_prefix, **kwargs)
        }

    @classmethod
    def partial_prefix_match(cls, **kwargs):
        matches = cls.partial_matches(is_prefix=True, **kwargs)

        min_num, min_cg = None, None

        for num, cg in matches.items():
            if min_num is None or len(cg) < len(min_cg):
                min_num, min_cg = num, cg

        return min_num, min_cg

    @classmethod
    def full_match(cls, **kwargs):
        full_matches = [
            (num, cg) for num, cg in cls.ALL.items() if cg._full_match(**kwargs)
        ]
        if not full_matches:
            return None, None
        if len(full_matches) > 1:
            raise ValueError(f"Internal Error, multiple matches for {kwargs}.")
        return full_matches[0]

    @classmethod
    def by_number(cls, num: str):
        return cls.ALL.get(num, None)

    @staticmethod
    def _create_all():
        key = CanonicalGeography.__init_key
        all_cgs = {
            "010": CanonicalGeography(["us"], key),
            "020": CanonicalGeography(["region"], key),
            "030": CanonicalGeography(["division"], key),
            "040": CanonicalGeography(["state"], key),
            "050": CanonicalGeography(["state", "county"], key),
            "060": CanonicalGeography(["state", "county", "county subdivision"], key),
            "067": CanonicalGeography(
                ["state", "county", "county subdivision", "subminor civil division"],
                key,
            ),
            "070": CanonicalGeography(
                ["state", "county", "county subdivision", "place/remainder (or part)"],
                key,
            ),
            "080": CanonicalGeography(
                ["state", "county", "county subdivision", "place ", "tract (or part)"],
                key,
            ),
            "101": CanonicalGeography(["state", "county", "tract", "block"], key),
            "140": CanonicalGeography(["state", "county", "tract"], key),
            "150": CanonicalGeography(["state", "county", "tract", "block group"], key),
            "155": CanonicalGeography(["state", "place", "county (or part)"], key),
            "160": CanonicalGeography(["state", "place"], key),
            "170": CanonicalGeography(["state", "consolidated city"], key),
            "172": CanonicalGeography(
                ["state", "consolidated city", "place (or part)"], key
            ),
            "230": CanonicalGeography(
                ["state", "alaska native regional corporation"], key
            ),
            "250": CanonicalGeography(
                ["american indian area/alaska native area/hawaiian home land"], key
            ),
            "251": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal subdivision/remainder",
                ],
                key,
            ),
            "252": CanonicalGeography(
                [
                    "american indian area/alaska native area (reservation or statistical entity only)"
                ],
                key,
            ),
            "254": CanonicalGeography(
                [
                    "american indian area (off-reservation trust land only)/hawaiian home land"
                ],
                key,
            ),
            "256": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract",
                ],
                key,
            ),
            "258": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract",
                    "tribal block group",
                ],
                key,
            ),
            "260": CanonicalGeography(
                ["american indian area/alaska native area/hawaiian home land", "state"],
                key,
            ),
            "269": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "state",
                    "place/remainder",
                ],
                key,
            ),
            "270": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "state",
                    "county",
                ],
                key,
            ),
            "280": CanonicalGeography(
                [
                    "state",
                    "american indian area/alaska native area/hawaiian home land (or part)",
                ],
                key,
            ),
            "281": CanonicalGeography(
                [
                    "state",
                    "american indian area",
                    "tribal subdivision/remainder (or part)",
                ],
                key,
            ),
            "283": CanonicalGeography(
                [
                    "state",
                    "american indian area/alaska native area (reservation or statistical entity only) (or part)",
                ],
                key,
            ),
            "286": CanonicalGeography(
                [
                    "state",
                    "american indian area (off-reservation trust land only)/hawaiian home land (or part)",
                ],
                key,
            ),
            "290": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal subdivision/remainder",
                    "state",
                ],
                key,
            ),
            "291": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract (or part) within aia (reservation only)",
                ],
                key,
            ),
            "292": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract (or part) within aia (trust land only)",
                ],
                key,
            ),
            "293": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract",
                    "tribal block group (or part) within tribal census tract within aia (reservation only)",
                ],
                key,
            ),
            "294": CanonicalGeography(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract",
                    "tribal block group (or part) within tribal census tract within aia (trust land only)",
                ],
                key,
            ),
            "310": CanonicalGeography(
                ["metropolitan statistical area/micropolitan statistical area"], key
            ),
            "311": CanonicalGeography(
                [
                    "metropolitan statistical area/micropolitan statistical area",
                    "state",
                ],
                key,
            ),
            "312": CanonicalGeography(
                [
                    "metropolitan statistical area/micropolitan statistical area",
                    "state",
                    "principal city",
                ],
                key,
            ),
            "314": CanonicalGeography(
                [
                    "metropolitan statistical area/micropolitan statistical area",
                    "metropolitan division",
                ],
                key,
            ),
            "315": CanonicalGeography(
                ["metropolitan statistical area", "metropolitan division", "state"], key
            ),
            "320": CanonicalGeography(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area (or part)",
                ],
                key,
            ),
            "321": CanonicalGeography(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area",
                    "principal city (or part)",
                ],
                key,
            ),
            "322": CanonicalGeography(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area",
                    "county",
                ],
                key,
            ),
            "323": CanonicalGeography(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area",
                    "metropolitan division (or part)",
                ],
                key,
            ),
            "324": CanonicalGeography(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area",
                    "metropolitan division",
                    "county",
                ],
                key,
            ),
            "330": CanonicalGeography(["combined statistical area"], key),
            "331": CanonicalGeography(["combined statistical area", "state"], key),
            "332": CanonicalGeography(
                ["combined statistical area", "micropolitan statistical area"], key
            ),
            "333": CanonicalGeography(
                [
                    "combined statistical area",
                    "metropolitan statistical area/micropolitan statistical area",
                    "state",
                ],
                key,
            ),
            "335": CanonicalGeography(["combined new england city and town area"], key),
            "336": CanonicalGeography(
                ["combined new england city and town area", "state"], key
            ),
            "337": CanonicalGeography(
                [
                    "combined new england city and town area",
                    "new england city and town area",
                ],
                key,
            ),
            "338": CanonicalGeography(
                [
                    "combined new england city and town area",
                    "new england city and town area",
                    "state",
                ],
                key,
            ),
            "340": CanonicalGeography(
                ["state", "combined statistical area (or part)"], key
            ),
            "341": CanonicalGeography(
                [
                    "state",
                    "combined statistical area",
                    "metropolitan statistical area/micropolitan statistical area (or part)",
                ],
                key,
            ),
            "345": CanonicalGeography(
                ["state", "combined new england city and town area (or part)"], key
            ),
            "346": CanonicalGeography(
                [
                    "state",
                    "combined new england city and town area",
                    "new england city and town area (or part)",
                ],
                key,
            ),
            "350": CanonicalGeography(["new england city and town area"], key),
            "351": CanonicalGeography(["new england city and town area", "state"], key),
            "352": CanonicalGeography(
                ["new england city and town area", "state", "principal city"], key
            ),
            "355": CanonicalGeography(
                ["new england city and town area", "necta division"], key
            ),
            "356": CanonicalGeography(
                ["new england city and town area", "necta division", "state"], key
            ),
            "360": CanonicalGeography(
                ["state", "new england city and town area (or part)"], key
            ),
            "361": CanonicalGeography(
                ["state", "new england city and town area", "place"], key
            ),
            "362": CanonicalGeography(
                ["state", "new england city and town area", "county (or part)"], key
            ),
            "363": CanonicalGeography(
                [
                    "state",
                    "new england city and town area",
                    "county",
                    "county subdivision",
                ],
                key,
            ),
            "364": CanonicalGeography(
                ["state", "new england city and town area", "necta division (or part)"],
                key,
            ),
            "365": CanonicalGeography(
                [
                    "state",
                    "new england city and town area",
                    "necta division",
                    "county (or part)",
                ],
                key,
            ),
            "366": CanonicalGeography(
                [
                    "state",
                    "new england city and town area",
                    "necta division",
                    "county",
                    "county subdivision",
                ],
                key,
            ),
            "400": CanonicalGeography(["urban area"], key),
            "410": CanonicalGeography(["urban area", "state"], key),
            "430": CanonicalGeography(["urban area", "state", "county"], key),
            "500": CanonicalGeography(["state", "congressional district"], key),
            "510": CanonicalGeography(
                ["state", "congressional district", "county"], key
            ),
            "511": CanonicalGeography(
                ["state", "congressional district", "county", "tract"], key
            ),
            "521": CanonicalGeography(
                ["state", "congressional district", "county", "county subdivision"], key
            ),
            "531": CanonicalGeography(
                ["state", "congressional district", "place"], key
            ),
            "550": CanonicalGeography(
                [
                    "state",
                    "congressional district",
                    "american indian area/alaska native area/hawaiian home land",
                ],
                key,
            ),
            "560": CanonicalGeography(
                [
                    "state",
                    "congressional district",
                    "alaska native regional corporation",
                ],
                key,
            ),
            "610": CanonicalGeography(
                ["state", "state legislative district (upper chamber)"], key
            ),
            "612": CanonicalGeography(
                ["state", "state legislative district (upper chamber)", "county"], key
            ),
            "620": CanonicalGeography(
                ["state", "state legislative district (lower chamber)"], key
            ),
            "622": CanonicalGeography(
                [
                    "state",
                    "state legislative district (lower chamber)",
                    "county (or part)",
                ],
                key,
            ),
            "795": CanonicalGeography(["state", "public use microdata area"], key),
            "860": CanonicalGeography(["zip code tabulation area"], key),
            "871": CanonicalGeography(
                ["state", "zip code tabulation area (or part)"], key
            ),
            "950": CanonicalGeography(["state", "school district (elementary)"], key),
            "960": CanonicalGeography(["state", "school district (secondary)"], key),
            "970": CanonicalGeography(["state", "school district (unified)"], key),
        }
        return all_cgs


CanonicalGeography.ALL = CanonicalGeography._create_all()
