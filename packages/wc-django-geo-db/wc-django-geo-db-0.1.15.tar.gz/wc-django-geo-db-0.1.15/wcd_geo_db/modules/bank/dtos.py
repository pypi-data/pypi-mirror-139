from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence
from django.contrib.gis.geos import Point, MultiPolygon

from wcd_geo_db.const import DivisionLevel


__all__ = (
    'GeometryDTO',
    'NamePrefixDTO',
    'DivisionDTO',
    'ExtendedDivisionDTO',
    'DivisionTranslationDTO',
)


@dataclass
class GeometryDTO:
    location: Optional[Point]
    polygon: Optional[MultiPolygon]


@dataclass
class NamePrefixDTO:
    name: str = ''
    short: str = ''


@dataclass
class DivisionDTO:
    id: int
    name: str
    label: str
    level: DivisionLevel
    types: List[str]
    codes: dict
    parent_id: int
    path: Sequence[int]


@dataclass
class ExtendedDivisionDTO(DivisionDTO):
    prefix: NamePrefixDTO
    geometry: GeometryDTO


@dataclass
class DivisionTranslationDTO:
    id: int
    language: str
    entity_id: int
    name: str
