from typing import Any, List, Optional, Sequence, TypeVar
from django.db import models
from django.db.models.fields import BooleanField, IntegerField
from django.db.models.functions import Cast
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest

from wcd_geo_db.const import DivisionLevel
from wcd_geo_db.modules.code_seeker.query import CodeSeekerQuerySet
from pxd_tree.hierarchy import TreeQuerySet

from ..dtos import DivisionDTO, ExtendedDivisionDTO, GeometryDTO, NamePrefixDTO
from .base import QuerySet
from .geometry import WithGeometryQuerySet
from .search import SearchQueryParam, SearchQuerySet
from .dto import DTOResolverQuerysetMixin


__all__ = 'DivisionsQuerySet',

QT = TypeVar('QT', bound='DivisionsQuerySet')
VALUES_NAMES = (
    'id', 'name', 'label', 'level', 'types', 'codes', 'parent_id', 'path',
)
EXTENDED_VALUES_NAMES = VALUES_NAMES + (
    'prefix_id', 'location', 'polygon',
)
PREFIX_VALUES_NAMES = 'id', 'name', 'short',


# TODO: Rework.
def extended_as_dto(values: dict, prefixes: dict) -> 'ExtendedDivisionDTO':
    pget = (prefixes.get(values['prefix_id']) or {}).get

    return ExtendedDivisionDTO(
        id=values['id'],
        name=values['name'],
        label=values['label'],
        prefix=NamePrefixDTO(name=pget('name', ''), short=pget('short', '')),
        level=DivisionLevel(values['level']),
        types=values['types'],
        codes=values['codes'],
        parent_id=values['parent_id'],
        path=list(values['path']),
        geometry=GeometryDTO(
            location=values['location'],
            polygon=values['polygon'],
        )
    )


def extended_dto_resolver(query, **kwargs) -> List['ExtendedDivisionDTO']:
    from wcd_geo_db.modules.bank.db import DivisionPrefix

    values = query.values(*EXTENDED_VALUES_NAMES)
    prefixes = {
        x['id']: x
        for x in DivisionPrefix.objects.all().values(*PREFIX_VALUES_NAMES)
    }

    return [extended_as_dto(values, prefixes=prefixes) for values in values]


def base_as_dto(values: dict) -> 'DivisionDTO':
    return DivisionDTO(
        id=values['id'],
        name=values['name'],
        label=values['label'],
        level=DivisionLevel(values['level']),
        types=values['types'],
        codes=values['codes'],
        parent_id=values['parent_id'],
        path=list(values['path']),
    )


def base_dto_resolver(query, **kwargs) -> List['DivisionDTO']:
    values = query.values(*VALUES_NAMES)
    return [base_as_dto(values) for values in values]


class DivisionsQuerySet(
    DTOResolverQuerysetMixin,
    WithGeometryQuerySet,
    CodeSeekerQuerySet,
    TreeQuerySet,
    SearchQuerySet,
    QuerySet
):
    SEARCH_QUERY_MIN_LENGTH: int = 1
    SEARCH_QUERY_MIN_RANK: float = 0.1
    SEARCH_QUERY_RANK_WEIGHTS: Sequence[float] = [0.2, 0.4, 0.8, 1]

    # TODO: Rework.
    dto_default_resolvers = {
        DivisionDTO: base_dto_resolver,
        ExtendedDivisionDTO: extended_dto_resolver,
    }

    def _search_rank_order(self: QT, query: SearchQueryParam) -> QT:
        q = query.get('query')
        min_rank = query.get('min_rank', self.SEARCH_QUERY_MIN_RANK)

        name_equality = models.Case(
            models.When(name__iexact=q, then=models.Value(1)),
            models.When(translations__name__iexact=q, then=models.Value(1)),
            default=models.Value(0),
            output_field=models.IntegerField()
        )
        name_similarity = Greatest(
            TrigramSimilarity(
                'name', Cast(models.Value(q), output_field=models.TextField()),
                function='strict_word_similarity'
            ),
            TrigramSimilarity(
                'translations__name', Cast(models.Value(q), output_field=models.TextField()),
                function='strict_word_similarity'
            ),
        )
        synonyms_similarity = Greatest(
            TrigramSimilarity(
                'synonyms', Cast(models.Value(q), output_field=models.TextField()),
                function='strict_word_similarity'
            ),
            TrigramSimilarity(
                'translations__synonyms', Cast(models.Value(q), output_field=models.TextField()),
                function='strict_word_similarity'
            ),
        )

        queryset = (
            self
            .annotate(
                name_equality=name_equality,
                name_similarity=name_similarity,
                synonyms_similarity=synonyms_similarity,
            )
            .filter(
                models.Q(name_equality=1)
                |
                models.Q(name_similarity__gt=min_rank)
                |
                models.Q(synonyms_similarity__gt=min_rank)
            )
            .order_by('-name_equality', '-name_similarity', '-synonyms_similarity')
        )

        return queryset

    def _search_simple_similarity(self: QT, query: SearchQueryParam) -> QT:
        q = query.get('query')

        name_equality = models.Case(
            models.When(name__iexact=q, then=models.Value(1)),
            models.When(translations__name__iexact=q, then=models.Value(1)),
            default=models.Value(0),
            output_field=models.IntegerField()
        )

        queryset = (
            self
            .annotate(name_equality=name_equality)
            .filter(
                models.Q(name_equality=1)
                |
                models.Q(name__icontains=q)
                |
                models.Q(translations__name__icontains=q)
            )
            .order_by('-name_equality')
        )

        return queryset

    def search(self: QT, query: SearchQueryParam) -> QT:
        q = query.get('query')

        if not q or len(q) < self.SEARCH_QUERY_MIN_LENGTH:
            return self

        if query.get('use_simple_search'):
            return self._search_simple_similarity(query)

        return self._search_rank_order(query)

    def general_filter(
        self: QT,
        parent_ids: Optional[Sequence[int]] = None,
        labels: Optional[Sequence[str]] = None,
        levels: Optional[Sequence[DivisionLevel]] = None,
        types: Optional[Sequence[str]] = None,
        **kw
    ) -> QT:
        q = (
            super().general_filter(**kw)
            .optional_in('parent_id', parent_ids)
            .optional_in('label', labels)
            .optional_in('level', levels)
            .optional_overlap('types', types)
        )

        return q
