from typing import ClassVar, Iterable, List, Mapping, Optional, Tuple, Union
from dataclasses import dataclass

InSpecType = Union[str, Iterable[str]]


class PathSpec:

    # We hide this object inside the class to make __init__
    # effectively private. If you don't have access to this
    # key you can't successfully call __init___.
    __init_key = object()

    def __init__(self, path: Iterable[str], init_key: Optional = None):
        if init_key is not PathSpec.__init_key:
            raise ValueError(
                "CanonicalGeographies cannot be created directly. "
                "Try `PathSpec.partial_matches(**kwargs)` or "
                "`PathSpec.full_match(**kwargs) instead."
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

    def _partial_match(
        self,
        is_prefix: bool = True,
        **kwargs: InSpecType,
    ) -> bool:
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

    def fill_in(self, **kwargs: InSpecType) -> InSpecType:
        if not self._partial_match(is_prefix=False, **kwargs):
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
    def partial_matches(
        cls, is_prefix=True, **kwargs: InSpecType
    ) -> List["BoundGeographyPath"]:
        kwargs = PathSpec._u2s(**kwargs)

        return [
            BoundGeographyPath(num, path_spec, **kwargs)
            for num, path_spec in cls.ALL.items()
            if path_spec._partial_match(is_prefix, **kwargs)
        ]

    @classmethod
    def partial_prefix_match(cls, **kwargs: InSpecType) -> "BoundGeographyPath":
        matches = cls.partial_matches(is_prefix=True, **kwargs)

        min_num, min_bgp = None, None

        for bgp in matches:
            if min_num is None or len(bgp.path_spec) < min_num:
                min_num, min_bgp = len(bgp.path_spec), bgp

        return min_bgp

    @classmethod
    def full_match(cls, **kwargs: InSpecType):
        full_matches = [
            (num, path_spec)
            for num, path_spec in cls.ALL.items()
            if path_spec._full_match(**kwargs)
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
        key = PathSpec.__init_key
        all_path_specs = {
            "010": PathSpec(["us"], key),
            "020": PathSpec(["region"], key),
            "030": PathSpec(["division"], key),
            "040": PathSpec(["state"], key),
            "050": PathSpec(["state", "county"], key),
            "060": PathSpec(["state", "county", "county subdivision"], key),
            "067": PathSpec(
                ["state", "county", "county subdivision", "subminor civil division"],
                key,
            ),
            "070": PathSpec(
                ["state", "county", "county subdivision", "place/remainder (or part)"],
                key,
            ),
            "080": PathSpec(
                ["state", "county", "county subdivision", "place ", "tract (or part)"],
                key,
            ),
            "101": PathSpec(["state", "county", "tract", "block"], key),
            "140": PathSpec(["state", "county", "tract"], key),
            "150": PathSpec(["state", "county", "tract", "block group"], key),
            "155": PathSpec(["state", "place", "county (or part)"], key),
            "160": PathSpec(["state", "place"], key),
            "170": PathSpec(["state", "consolidated city"], key),
            "172": PathSpec(["state", "consolidated city", "place (or part)"], key),
            "230": PathSpec(["state", "alaska native regional corporation"], key),
            "250": PathSpec(
                ["american indian area/alaska native area/hawaiian home land"], key
            ),
            "251": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal subdivision/remainder",
                ],
                key,
            ),
            "252": PathSpec(
                [
                    "american indian area/alaska native area (reservation or statistical entity only)"
                ],
                key,
            ),
            "254": PathSpec(
                [
                    "american indian area (off-reservation trust land only)/hawaiian home land"
                ],
                key,
            ),
            "256": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract",
                ],
                key,
            ),
            "258": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract",
                    "tribal block group",
                ],
                key,
            ),
            "260": PathSpec(
                ["american indian area/alaska native area/hawaiian home land", "state"],
                key,
            ),
            "269": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "state",
                    "place/remainder",
                ],
                key,
            ),
            "270": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "state",
                    "county",
                ],
                key,
            ),
            "280": PathSpec(
                [
                    "state",
                    "american indian area/alaska native area/hawaiian home land (or part)",
                ],
                key,
            ),
            "281": PathSpec(
                [
                    "state",
                    "american indian area",
                    "tribal subdivision/remainder (or part)",
                ],
                key,
            ),
            "283": PathSpec(
                [
                    "state",
                    "american indian area/alaska native area (reservation or statistical entity only) (or part)",
                ],
                key,
            ),
            "286": PathSpec(
                [
                    "state",
                    "american indian area (off-reservation trust land only)/hawaiian home land (or part)",
                ],
                key,
            ),
            "290": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal subdivision/remainder",
                    "state",
                ],
                key,
            ),
            "291": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract (or part) within aia (reservation only)",
                ],
                key,
            ),
            "292": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract (or part) within aia (trust land only)",
                ],
                key,
            ),
            "293": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract",
                    "tribal block group (or part) within tribal census tract within aia (reservation only)",
                ],
                key,
            ),
            "294": PathSpec(
                [
                    "american indian area/alaska native area/hawaiian home land",
                    "tribal census tract",
                    "tribal block group (or part) within tribal census tract within aia (trust land only)",
                ],
                key,
            ),
            "310": PathSpec(
                ["metropolitan statistical area/micropolitan statistical area"], key
            ),
            "311": PathSpec(
                [
                    "metropolitan statistical area/micropolitan statistical area",
                    "state",
                ],
                key,
            ),
            "312": PathSpec(
                [
                    "metropolitan statistical area/micropolitan statistical area",
                    "state",
                    "principal city",
                ],
                key,
            ),
            "314": PathSpec(
                [
                    "metropolitan statistical area/micropolitan statistical area",
                    "metropolitan division",
                ],
                key,
            ),
            "315": PathSpec(
                ["metropolitan statistical area", "metropolitan division", "state"], key
            ),
            "320": PathSpec(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area (or part)",
                ],
                key,
            ),
            "321": PathSpec(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area",
                    "principal city (or part)",
                ],
                key,
            ),
            "322": PathSpec(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area",
                    "county",
                ],
                key,
            ),
            "323": PathSpec(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area",
                    "metropolitan division (or part)",
                ],
                key,
            ),
            "324": PathSpec(
                [
                    "state",
                    "metropolitan statistical area/micropolitan statistical area",
                    "metropolitan division",
                    "county",
                ],
                key,
            ),
            "330": PathSpec(["combined statistical area"], key),
            "331": PathSpec(["combined statistical area", "state"], key),
            "332": PathSpec(
                ["combined statistical area", "micropolitan statistical area"], key
            ),
            "333": PathSpec(
                [
                    "combined statistical area",
                    "metropolitan statistical area/micropolitan statistical area",
                    "state",
                ],
                key,
            ),
            "335": PathSpec(["combined new england city and town area"], key),
            "336": PathSpec(["combined new england city and town area", "state"], key),
            "337": PathSpec(
                [
                    "combined new england city and town area",
                    "new england city and town area",
                ],
                key,
            ),
            "338": PathSpec(
                [
                    "combined new england city and town area",
                    "new england city and town area",
                    "state",
                ],
                key,
            ),
            "340": PathSpec(["state", "combined statistical area (or part)"], key),
            "341": PathSpec(
                [
                    "state",
                    "combined statistical area",
                    "metropolitan statistical area/micropolitan statistical area (or part)",
                ],
                key,
            ),
            "345": PathSpec(
                ["state", "combined new england city and town area (or part)"], key
            ),
            "346": PathSpec(
                [
                    "state",
                    "combined new england city and town area",
                    "new england city and town area (or part)",
                ],
                key,
            ),
            "350": PathSpec(["new england city and town area"], key),
            "351": PathSpec(["new england city and town area", "state"], key),
            "352": PathSpec(
                ["new england city and town area", "state", "principal city"], key
            ),
            "355": PathSpec(["new england city and town area", "necta division"], key),
            "356": PathSpec(
                ["new england city and town area", "necta division", "state"], key
            ),
            "360": PathSpec(["state", "new england city and town area (or part)"], key),
            "361": PathSpec(["state", "new england city and town area", "place"], key),
            "362": PathSpec(
                ["state", "new england city and town area", "county (or part)"], key
            ),
            "363": PathSpec(
                [
                    "state",
                    "new england city and town area",
                    "county",
                    "county subdivision",
                ],
                key,
            ),
            "364": PathSpec(
                ["state", "new england city and town area", "necta division (or part)"],
                key,
            ),
            "365": PathSpec(
                [
                    "state",
                    "new england city and town area",
                    "necta division",
                    "county (or part)",
                ],
                key,
            ),
            "366": PathSpec(
                [
                    "state",
                    "new england city and town area",
                    "necta division",
                    "county",
                    "county subdivision",
                ],
                key,
            ),
            "400": PathSpec(["urban area"], key),
            "410": PathSpec(["urban area", "state"], key),
            "430": PathSpec(["urban area", "state", "county"], key),
            "500": PathSpec(["state", "congressional district"], key),
            "510": PathSpec(["state", "congressional district", "county"], key),
            "511": PathSpec(
                ["state", "congressional district", "county", "tract"], key
            ),
            "521": PathSpec(
                ["state", "congressional district", "county", "county subdivision"], key
            ),
            "531": PathSpec(["state", "congressional district", "place"], key),
            "550": PathSpec(
                [
                    "state",
                    "congressional district",
                    "american indian area/alaska native area/hawaiian home land",
                ],
                key,
            ),
            "560": PathSpec(
                [
                    "state",
                    "congressional district",
                    "alaska native regional corporation",
                ],
                key,
            ),
            "610": PathSpec(
                ["state", "state legislative district (upper chamber)"], key
            ),
            "612": PathSpec(
                ["state", "state legislative district (upper chamber)", "county"], key
            ),
            "620": PathSpec(
                ["state", "state legislative district (lower chamber)"], key
            ),
            "622": PathSpec(
                [
                    "state",
                    "state legislative district (lower chamber)",
                    "county (or part)",
                ],
                key,
            ),
            "795": PathSpec(["state", "public use microdata area"], key),
            "860": PathSpec(["zip code tabulation area"], key),
            "871": PathSpec(["state", "zip code tabulation area (or part)"], key),
            "950": PathSpec(["state", "school district (elementary)"], key),
            "960": PathSpec(["state", "school district (secondary)"], key),
            "970": PathSpec(["state", "school district (unified)"], key),
        }
        return all_path_specs


PathSpec.ALL = PathSpec._create_all()


class BoundGeographyPath:
    def __init__(self, num: str, path_spec: PathSpec, **kwargs: InSpecType):
        self._num = num
        self._path_spec = path_spec
        self._bindings = path_spec.fill_in(**kwargs)

    @property
    def num(self) -> str:
        return self._num

    @property
    def path_spec(self) -> PathSpec:
        return self._path_spec

    @property
    def bindings(self) -> Mapping[str, InSpecType]:
        return self._bindings


@dataclass(frozen=True)
class CensusGeographyQuerySpec:

    source: str
    year: int
    fields: List[str]
    bound_path: BoundGeographyPath
    api_key: Optional[str] = None

    _BASE_URL: ClassVar[str] = "https://api.census.gov/data"

    @property
    def for_component(self) -> str:
        *_, (k, v) = self.bound_path.bindings.items()
        if v == "*":
            return f"{k}"
        return f"{k}:{v}"

    @property
    def in_components(self) -> str:
        *components, _ = self.bound_path.bindings.items()

        if components:
            return " ".join(f"{k}:{v}" for (k, v) in components)

        return None

    def detail_table_url(self) -> Tuple[str, Mapping[str, str]]:
        url = "/".join([self._BASE_URL, f"{self.year:04}", self.source])

        params = {
            "get": ",".join(self.fields),
            "for": self.for_component,
        }

        in_components = self.in_components
        if in_components is not None:
            params["in"] = in_components

        if self.api_key is not None:
            params["key"] = self.api_key

        return url, params
