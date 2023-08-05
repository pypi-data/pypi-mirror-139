from decimal import Decimal
from typing import Any, List, Optional, Tuple, TypedDict

from wcd_geo_db.const import DivisionLevel, DivisionType


__all__ = 'CodesItem', 'DivisionItem', 'DivisionTranslationItem',


class CodesItem(TypedDict):
    code: Tuple[str, Any]
    codes: List[Tuple[str, Any]]


Point = Tuple[Decimal, Decimal]
"""[latitude, longitude]"""
Polygon = str


class DivisionItem(CodesItem, TypedDict):
    path: List[Tuple[str, Any]]
    name: Optional[str]
    name_prefix: Optional[str]
    synonyms: Optional[str]
    types: List[DivisionType]
    level: DivisionLevel
    location: Optional[Point]
    polygon: Optional[Polygon]


class DivisionTranslationItem(TypedDict):
    language: Optional[str]
    code: Tuple[str, Any]
    name: Optional[str]
    synonyms: Optional[str]
