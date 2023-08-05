from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, TYPE_CHECKING
from functools import cached_property
from django.db.models import F
from px_client_builder import NestedClient
from wcd_geo_db.modules.code_seeker.query import CodeSeekSeq

from ...bank.dtos import DivisionDTO, DivisionTranslationDTO
from ..dtos import AddressDefinitionDTO, FormattedAddressDTO

if TYPE_CHECKING:
    from ...bank import BankClient


__all__ = 'FormatterClient',


class FormatterClient(NestedClient):
    NAME_PREFIX_MAX_LENGTH: str = 6

    _bank_lookup: Callable

    def __init__(self, *_, bank_lookup: Callable = None, **kw):
        assert bank_lookup is not None, 'Bank lookuper is mandatory.'

        super().__init__(**kw)

        self._bank_lookup = bank_lookup

    bank: 'BankClient' = cached_property(lambda x: x._bank_lookup(x))

    # TODO: Make result formatters pluggable, because for different languages
    # they must be different.
    def _make_formatted_address(
        self,
        definition: AddressDefinitionDTO,
        divisions_map: Dict[int, DivisionDTO] = {},
        translations_map: Dict[int, DivisionTranslationDTO] = {},
        prefixes_map: Dict[int, dict] = {},
    ) -> Optional[FormattedAddressDTO]:
        path = definition.get('divisions_path')

        if not path:
            return None

        def add_prefix(id, string):
            data = prefixes_map.get(id, {})
            prefix = data.get('short') or ''

            if not prefix:
                prefix = data.get('name') or ''

                if len(prefix) > self.NAME_PREFIX_MAX_LENGTH:
                    prefix = ''

            if prefix:
                return f'{prefix} {string}'

            return string

        divisions = [
            translations_map.get(id, None) or divisions_map[id]
            for id in path
            if id in translations_map or id in divisions_map
        ]

        return FormattedAddressDTO(
            id=str(path[-1]),
            divisions=divisions,
            formatted_address=', '.join(
                add_prefix(getattr(d, 'entity_id', d.id), d.name)
                for d in reversed(divisions)
            )
        )

    def _normalize_address_definitions(
        definitions: Sequence[AddressDefinitionDTO],
    ) -> Tuple[Sequence[AddressDefinitionDTO], dict]:
        return definitions

    def _get_prefixes_map(
        self,
        ids: List[int],
        language: str,
        fallback_languages: Sequence[str] = [],
    ):
        # FIXME: Change division prefixes resolver.
        # It should depend on client, without direct database usage.
        # Make all algorithm more efficient.
        from wcd_geo_db.modules.bank.db import DivisionPrefix, DivisionPrefixTranslation
        values = 'r_id', 'name', 'short'

        translations = (
            DivisionPrefixTranslation.objects
            .filter(entity__divisions__id__in=ids)
            .annotate(r_id=F('entity__divisions__id'))
        )

        if fallback_languages:
            translations = translations.by_language_order(*[language] + fallback_languages)
        else:
            translations = translations.by_language(language)

        translations = list(translations.values(*values))
        diff = ids - {x['r_id'] for x in translations}

        if diff:
            translations += list(
                DivisionPrefix.objects
                .filter(divisions__id__in=diff)
                .annotate(r_id=F('divisions__id'))
                .values(*values)
            )

        return {x['r_id']: x for x in translations}

    def format_addresses(
        self,
        definitions: Sequence[AddressDefinitionDTO],
        language: str,
        fallback_languages: Sequence[str] = [],
    ) -> Sequence[Optional[FormattedAddressDTO]]:
        """Formats addresses definitions.

        Result will be in the same order as passed in definitions.
        If address can't be formatted pastes None on it's place.
        """
        definitions: Sequence[AddressDefinitionDTO] = list(definitions)
        division_ids = set()
        divisions = []

        for definition in definitions:
            # FIXME: Made an adequate normalization that wouldn't
            # mutate initial structure.
            path = definition['divisions_path'] = list(definition.get('divisions_path') or ())

            for i, division in enumerate(path):
                if division is None:
                    continue

                if isinstance(division, int):
                    division_ids.add(division)
                elif isinstance(division, DivisionDTO):
                    divisions.append(division)
                    division_ids.add(division.id)
                    path[i] = division.id
                else:
                    raise TypeError(
                        f'Wrong division in path: {type(division)}, {repr(division)}.'
                    )

        # FIXME: A little bit inefficient.
        # There must be a way to fallback to division names if no translation
        # here in on query.
        translations = self.bank.divisions.get_translations(
            ids=division_ids,
            language=language, fallback_languages=fallback_languages
        )
        translations_map = {t.entity_id: t for t in translations}

        no_translated_ids = division_ids - translations_map.keys()

        if len(no_translated_ids) > 0:
            divisions += list(self.bank.divisions.get(ids=no_translated_ids))

        divisions_map = {d.id: d for d in divisions}

        return [
            self._make_formatted_address(
                definition,
                divisions_map=divisions_map,
                translations_map=translations_map,
                prefixes_map=self._get_prefixes_map(
                    translations_map.keys() | divisions_map.keys(),
                    language=language,
                    fallback_languages=fallback_languages,
                ),
            )
            for definition in definitions
        ]
