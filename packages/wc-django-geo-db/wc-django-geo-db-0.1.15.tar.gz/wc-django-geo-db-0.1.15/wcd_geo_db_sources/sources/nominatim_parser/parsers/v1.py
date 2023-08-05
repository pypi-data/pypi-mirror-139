import json
import marshal
from typing import TYPE_CHECKING, TextIO, Tuple, TypedDict, List, Optional
from django.conf import settings

from wcd_geo_db_sources.modules.merger.dtos import DivisionItem, DivisionTranslationItem, Point, Polygon
from wcd_geo_db.modules.code_seeker.builtins import ISO3166_SEEKER
from wcd_geo_db_sources.sources.geonames.code_seeker import GEONAMES_SEEKER
from wcd_geo_db_sources.sources.wikidata.code_seeker import WIKIDATA_SEEKER
from wcd_geo_db_sources.sources.openstreetmap.code_seeker import OPENSTREETMAP_SEEKER
from wcd_geo_db_sources.sources.koatuu.code_seeker import KOATUU_SEEKER
from wcd_geo_db_sources.sources.katottg.code_seeker import KATOTTG_SEEKER
from wcd_geo_db_sources.sources.postcode.code_seeker import POSTCODE_SEEKER
from ..._base.parser import json_encoder

if TYPE_CHECKING:
    from ..process import NOMINATIMImportRunner


def resolve_postcodes(code: Optional[str]):
    if not code:
        return []

    multiple = code.split(',')

    if len(multiple) > 1:
        return [x for y in multiple for x in resolve_postcodes(y)]

    rng = code.split('-')

    if len(rng) != 2:
        return rng[0]

    code_from, code_to = map(int, rng)

    return [str(x) for x in range(code_from, code_to + 1)]


AVAILABLE_LANGUAGES = {x for x, _ in settings.LANGUAGES}
UA_CODE = 'UA'
LOCAL_LANGUAGE = 'uk'
USABLE_OSM_TYPES = {'relation', 'r', 'node', 'n', }
USABLE_CATEGORIES = {'place', 'boundary', }
EXCLUDE_TYPES = {'historic', 'square', 'suburb'}
CODES_SOLVERS = (
    # (POSTCODE_SEEKER, lambda x: resolve_postcodes(
    #     x.get('calculated_postcode') or None
    # )),
    (GEONAMES_SEEKER, lambda x: [(x.get('extratags') or {}).get('geonameid') or None]),
    (ISO3166_SEEKER, lambda x: [(x.get('extratags') or {}).get('ISO3166-1:alpha2') or None]),
    (KATOTTG_SEEKER, lambda x: [(x.get('extratags') or {}).get('katotth') or None]),
    (KOATUU_SEEKER, lambda x: [(x.get('extratags') or {}).get('koatuu') or None]),
    (WIKIDATA_SEEKER, lambda x: [(x.get('extratags') or {}).get('wikidata') or None]),
)
POSSIBLE_NAMES = 'old_name', 'official_name', 'alt_name',
TRP = 'name:'


class Geo(DivisionItem):
    place_id: str
    parent_place_id: str


class SourceData(TypedDict):
    pass


ResultItem = Tuple[Geo, List[DivisionTranslationItem]]


def resolve_synonyms(data: dict, language: Optional[str], actual):
    synonyms = set()
    postfix = ':' + (language or '')

    for name in POSSIBLE_NAMES:
        value = data.get(name + postfix)

        if value and value != actual:
            synonyms.add(value)

    return synonyms


def to_point(source) -> Point:
    lon, lat = source

    return lat, lon


def resolve_point(info: SourceData) -> Optional[Point]:
    if 'centroid' in info and info['centroid']['type'] == 'Point':
        return to_point(info['centroid']['coordinates'])
    return None


def resolve_polygon(info: SourceData) -> Optional[Polygon]:
    geojson = None

    if 'geojson' in info and info['geojson']:
        geojson = info['geojson']

    if 'geometry' in info and info['geometry']:
        geojson = info['geometry']

    if geojson and geojson.get('type') in {'Polygon', 'MultiPolygon'}:
        return json.dumps(geojson)

    return None


def resolve_codes(info: SourceData):
    osm_code = (OPENSTREETMAP_SEEKER.name, str(info['osm_id']))
    codes = [osm_code]

    for seeker, resolver in CODES_SOLVERS:
        values = resolver(info)

        for value in values:
            if value:
                codes.append((seeker.name, value))

    return osm_code, codes


def resolve_names(info: SourceData):
    names: dict = info.get('names', {})
    name = names.get('name') or info.get('localname')
    names.setdefault('name', name)
    names.setdefault(TRP + LOCAL_LANGUAGE, name)

    return name, names


def make_geo(data: dict):
    info: SourceData = data.get('detail_data') or data.get('search_data') or data
    osm_type = info.get('osm_type') or ''
    category = info.get('category') or ''
    type = info.get('type') or ''

    if not osm_type or osm_type.lower() not in USABLE_OSM_TYPES:
        return

    if not category or category.lower() not in USABLE_CATEGORIES:
        return

    if not type or type.lower() in EXCLUDE_TYPES:
        return

    osm_code, codes = resolve_codes(info)
    name, names = resolve_names(info)

    geo: Geo = Geo(
        code=osm_code,
        place_id=info.get('place_id', None),
        parent_place_id=info.get('parent_place_id', None),
        codes=codes,
        path=[osm_code],
        name=name,
        # Fake level. This must not be used to change level yet.
        level=None,
        location=resolve_point(info),
        polygon=resolve_polygon(info),
        name_prefix=names.get('name:prefix', None) or (info.get('extratags') or {}).get('name:prefix') or None,
        synonyms=','.join(
            resolve_synonyms(names, LOCAL_LANGUAGE, name)
            |
            resolve_synonyms(names, None, name)
        )
    )

    TRP = 'name:'
    l = len(TRP)
    translations: List[DivisionTranslationItem] = []

    for k, value in names.items():
        if not k.startswith(TRP):
            continue

        lang = k[l:]

        if lang not in AVAILABLE_LANGUAGES:
            continue

        translations.append(DivisionTranslationItem(
            language=lang, code=osm_code, name=value,
            synonyms=','.join(resolve_synonyms(names, lang, value))
        ))

    yield (geo, translations)

    if 'address' in info:
        for item in info['address']:
            for r in make_geo(item):
                yield r


def order_key(item: ResultItem):
    return (len(item[0]['path']), item[0]['code'])


def prepare_data(data, index: set):
    result = [y for x in data for y in make_geo(x)]

    return result


def parse(runner: 'NOMINATIMImportRunner', file: TextIO, into: str, first: bool = False):
    index_file = into + '.index'

    try:
        with open(index_file, 'rb') as f:
            parsed_index = marshal.load(f)
    except (FileNotFoundError, EOFError, ValueError, TypeError) as e:
        print(e)
        parsed_index = set()

    dfs = json.loads(file.read())

    prepared = prepare_data(dfs.values(), index=parsed_index)
    items = list(sorted(prepared, key=order_key))

    with open(index_file, 'wb') as f:
        marshal.dump(parsed_index, f)

    with open(into, 'a') as tmp:
        data = json.dumps(items, default=json_encoder)[1:-1]

        if data and not first:
            tmp.write(',')

        tmp.write(data)

    return tmp.name
