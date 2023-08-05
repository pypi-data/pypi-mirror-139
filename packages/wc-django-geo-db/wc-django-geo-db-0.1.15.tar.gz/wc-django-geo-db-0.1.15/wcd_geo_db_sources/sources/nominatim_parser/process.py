import json
from pprint import pprint
from itertools import groupby
import tempfile
from typing import Dict, List
from django.db import transaction
from pathlib import Path

from wcd_geo_db.const import DivisionLevel
from wcd_geo_db_sources.modules.process import stage
from wcd_geo_db_sources.modules.merger.divisions import (
    merge_divisions, merge_division_translations
)
from wcd_geo_db_sources.modules.merger.dtos import DivisionItem, DivisionTranslationItem
from wcd_geo_db.modules.code_seeker import ISO3166_SEEKER, registry as seeker_registry
from wcd_geo_db_sources.sources.katottg.code_seeker import KATOTTG_SEEKER
from wcd_geo_db_sources.sources.koatuu.code_seeker import KOATUU_SEEKER
from wcd_geo_db_sources.sources.novaposhta.const import Type

from wcd_geo_db_sources.sources.wikidata.code_seeker import WIKIDATA_SEEKER
from wcd_geo_db_sources.sources.openstreetmap.code_seeker import OPENSTREETMAP_SEEKER
from wcd_geo_db_sources.sources.koatuu.code_seeker import KOATUU_SEEKER
from wcd_geo_db_sources.sources.katottg.code_seeker import KATOTTG_SEEKER
from wcd_geo_db_sources.sources.postcode.code_seeker import POSTCODE_SEEKER
from wcd_geo_db.modules.code_seeker.builtins import ISO3166_SEEKER
from wcd_geo_db_sources.sources.geonames.code_seeker import GEONAMES_SEEKER

from .._base import BaseImportRunner
from .parsers.v1 import Geo
from .parsers import registry
from .const import SOURCE, ImportStage


SOURCE_PATH = (
    Path(__file__).parent.parent.parent.parent
    / 'data' / 'nominatim_parser' / 'storage2'
)
ADMINISTRATIVE_FILE_PATHS = (
    'administrative_isaddress/andreevskii-okrug_3827463.json',
    'administrative_isaddress/balaklavskii-okrug_3827446.json',
    'administrative_isaddress/balaklavskii-raion_3828424.json',
    'administrative_isaddress/darnitskii-raion_1754757.json',
    'administrative_isaddress/desnianskii-raion_1754820.json',
    'administrative_isaddress/dniprovskii-raion_1754781.json',
    'administrative_isaddress/gagarinskii-okrug_3827418.json',
    'administrative_isaddress/golosiyivskii-raion_1754513.json',
    'administrative_isaddress/inkerman_3827428.json',
    'administrative_isaddress/kachinskii-okrug_3827455.json',
    'administrative_isaddress/kiyiv_421866.json',
    'administrative_isaddress/leninskii-okrug_3827420.json',
    'administrative_isaddress/leninskii-raion_1753292.json',
    'administrative_isaddress/nakhimovskii-okrug_3827485.json',
    'administrative_isaddress/nakhimovskii-raion_3828338.json',
    'administrative_isaddress/obolonskii-raion_1754928.json',
    'administrative_isaddress/orlinovskii-okrug_3827426.json',
    'administrative_isaddress/pecherskii-raion_1755013.json',
    'administrative_isaddress/podilskii-raion_1754975.json',
    'administrative_isaddress/sevastopol_1574364.json',
    'administrative_isaddress/shevchenkivskii-raion_1755014.json',
    'administrative_isaddress/solomianskii-raion_1754514.json',
    'administrative_isaddress/sviatoshinskii-raion_1754751.json',
    'administrative_isaddress/ternovskii-okrug_3827429.json',
    'administrative_isaddress/ukrayina_60199.json',
    'administrative_isaddress/verkhnesadovskii-okrug_3827486.json',
)
UNGROUPED_FILE_PATHS = (
    'not_grouped/not_grouped.json',
)
STATE_FILE_PATHS = (
    'state/avtonomna-respublika-krim_72639.json',
    'state/cherkaska-oblast_91278.json',
    'state/cherkaska-oblast_91278_part_2.json',
    'state/chernigivska-oblast_71249.json',
    'state/chernigivska-oblast_71249_part_2.json',
    'state/chernivetska-oblast_72526.json',
    'state/dnipropetrovska-oblast_101746.json',
    'state/dnipropetrovska-oblast_101746_part_2.json',
    'state/dnipropetrovska-oblast_101746_part_3.json',
    'state/donetska-oblast_71973.json',
    'state/donetska-oblast_71973_part_2.json',
    'state/donetska-oblast_71973_part_3.json',
    'state/ivano-frankivska-oblast_72488.json',
    'state/ivano-frankivska-oblast_72488_part_2.json',
    'state/ivano-frankivska-oblast_72488_part_3.json',
    'state/kharkivska-oblast_71254.json',
    'state/kharkivska-oblast_71254_part_2.json',
    'state/kharkivska-oblast_71254_part_3.json',
    'state/khersonska-oblast_71022.json',
    'state/khmelnitska-oblast_90742.json',
    'state/khmelnitska-oblast_90742_part_2.json',
    'state/kirovogradska-oblast_101859.json',
    'state/kirovogradska-oblast_101859_part_2.json',
    'state/kiyivska-oblast_71248.json',
    'state/kiyivska-oblast_71248_part_2.json',
    'state/kiyivska-oblast_71248_part_3.json',
    'state/luganska-oblast_71971.json',
    'state/luganska-oblast_71971_part_2.json',
    'state/lvivska-oblast_72380.json',
    'state/lvivska-oblast_72380_part_2.json',
    'state/lvivska-oblast_72380_part_3.json',
    'state/lvivska-oblast_72380_part_4.json',
    'state/mikolayivska-oblast_72635.json',
    'state/mikolayivska-oblast_72635_part_2.json',
    'state/odeska-oblast_72634.json',
    'state/odeska-oblast_72634_part_2.json',
    'state/poltavska-oblast_91294.json',
    'state/poltavska-oblast_91294_part_2.json',
    'state/poltavska-oblast_91294_part_3.json',
    'state/respublika-krym_3795586.json',
    'state/rivnenska-oblast_71236.json',
    'state/rivnenska-oblast_71236_part_2.json',
    'state/sumska-oblast_71250.json',
    'state/sumska-oblast_71250_part_2.json',
    'state/ternopilska-oblast_72525.json',
    'state/ternopilska-oblast_72525_part_2.json',
    'state/ternopilska-oblast_72525_part_3.json',
    'state/vinnitska-oblast_90726.json',
    'state/vinnitska-oblast_90726_part_2.json',
    'state/volinska-oblast_71064.json',
    'state/volinska-oblast_71064_part_2.json',
    'state/zakarpatska-oblast_72489.json',
    'state/zakarpatska-oblast_72489_part_2.json',
    'state/zaporizka-oblast_71980.json',
    'state/zaporizka-oblast_71980_part_2.json',
    'state/zhitomirska-oblast_71245.json',
    'state/zhitomirska-oblast_71245_part_2.json',
    'state/zhitomirska-oblast_71245_part_3.json',
)
FILE_PATHS = ADMINISTRATIVE_FILE_PATHS + UNGROUPED_FILE_PATHS + STATE_FILE_PATHS
PARSER_VERSION = 'v1'
UKRAINIAN_LANGUAGE = 'uk'


class NOMINATIMImportRunner(BaseImportRunner):
    CHUNK_SIZE: int = 500
    source: str = SOURCE
    Stage: ImportStage = ImportStage
    default_config: dict = {
        'source_path': str(SOURCE_PATH),
        'source_files': FILE_PATHS,
        'version': PARSER_VERSION,
    }
    parser_registry: dict = registry

    @stage(Stage.INITIAL)
    def run_initial(self):
        self.update_state(stage=self.Stage.PARSING, partial_state={
            'source_path': self.config['source_path'],
            'source_files': self.config['source_files'],
            'version': self.config['version'],
        })

    @stage(Stage.PARSING)
    def run_parsing(self):
        state = self.state.state
        parse = self.parser_registry[state['version']]
        parsed_file = state.get('parsed_file')
        source_index = state.get('source_index', 0)
        source_files = state['source_files']
        first = parsed_file is None

        if first:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
                tmp.write('[')
            parsed_file = tmp.name

        if len(source_files) == source_index:
            with open(parsed_file, 'a') as file:
                file.write(']')

            return self.update_state(stage=self.Stage.MERGE, partial_state={
                'parsed_file': parsed_file,
            })

        source_file = Path(state['source_path']) / state['source_files'][source_index]

        with open(source_file, 'r') as file:
            parsed_file = parse(self, file=file, into=parsed_file, first=first)

        self.update_state(stage=self.Stage.PARSING, partial_state={
            'parsed_file': parsed_file, 'source_index': source_index + 1,
        })

    def remap_in_parents(self, items: List[Geo]):
        tree: Dict[str, set] = {}
        names = {}
        indexes = {}
        count = 0

        for i, (item, translations) in enumerate(items):
            p, c, n = item['parent_place_id'], item['place_id'], item['name']

            tree[p] = tree.get(p) or set()
            tree[p].add(c)
            names[n] = names.get(n) or set()
            names[n].add(c)
            indexes[c] = i

        def itm(num):
            return items[indexes[num]][0]

        for parent, values in tree.items():
            identical = {}
            cmp = values | {parent}

            for x in cmp:
                if x not in indexes: continue

                name = itm(x)['name']

                for y in cmp:
                    if y not in indexes: continue
                    if y == x: continue

                    if name == itm(y)['name']:
                        identical[name] = identical.get(name) or set()
                        identical[name].add(x)
                        identical[name].add(y)

            for name, ids in identical.items():
                if len(ids) != 2: continue

                prefixes = {itm(x)['name_prefix'] for x in ids}
                fc, tc = [{(c, v) for c, v in itm(x)['codes']} for x in ids]

                if len(fc.intersection(tc)) != 0: continue

                lens = (len(prefixes) == 1) or ((len(prefixes) == 2) and (None in prefixes))
                if not lens: continue

                empty = any(
                    not any(c not in ('OPENSTREETMAP', 'WIKIDATA') for c, val in itm(x)['codes'])
                    for x in ids
                )
                if not empty: continue

                count += 1

                f, t = [itm(x) for x in ids]
                f['codes'] = list(tc | fc)
                t['codes'] = f['codes']

        return items

    @stage(Stage.MERGE)
    def run_merge(self):
        state = self.state.state

        for seeker in (
            WIKIDATA_SEEKER, OPENSTREETMAP_SEEKER,
            KOATUU_SEEKER, KATOTTG_SEEKER,
            ISO3166_SEEKER, GEONAMES_SEEKER,
        ):
            if seeker.name not in seeker_registry:
                seeker_registry.register(seeker)

        offset = state.get('merge_offset', 0)
        chunk = []
        count = self.CHUNK_SIZE

        with open(state['parsed_file'], 'r') as file:
            items = json.loads(file.read())

        if offset == 0:
            items = self.remap_in_parents(items)

            with open(state['parsed_file'], 'w') as file:
                file.write(json.dumps(items))

        to = offset + count
        chunk = [geo for geo, _ in items[offset:to]]

        with transaction.atomic():
            merge_divisions(
                chunk,
                change_path=False, change_level=False, change_types=False,
                should_create=False, lookup_on_singular_name_equality=False,
                override_name=True, override_name_prefix=True,
            )
            self.update_state(partial_state={'merge_offset': to})

        if len(items) > to:
            return

        self.update_state(stage=self.Stage.MERGE_TRANSLATIONS)

    @stage(Stage.MERGE_TRANSLATIONS)
    def run_merge_translations(self):
        state = self.state.state

        for seeker in (
            WIKIDATA_SEEKER, OPENSTREETMAP_SEEKER,
            KOATUU_SEEKER, KATOTTG_SEEKER,
        ):
            if seeker.name not in seeker_registry:
                seeker_registry.register(seeker)

        offset = state.get('merge_translations_offset', 0)
        chunk = []
        count = self.CHUNK_SIZE

        with open(state['parsed_file'], 'r') as file:
            items = json.loads(file.read())
            next_offset = offset + count
            chunk = [
                translation
                for _, translations in items[offset:next_offset]
                for translation in translations
            ]
            key = lambda x: x['language']
            groups = groupby(sorted(chunk, key=key), key=key)

            with transaction.atomic():
                for language, grouped in groups:
                    merge_division_translations(language, list(grouped), override_name=True)

                self.update_state(partial_state={'merge_translations_offset': next_offset})

            if len(items) > next_offset:
                return

        self.update_state(stage=self.Stage.CLEANUP)
