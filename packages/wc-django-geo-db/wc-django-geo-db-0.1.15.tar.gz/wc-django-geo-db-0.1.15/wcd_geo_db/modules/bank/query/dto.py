from typing import Callable, Dict, List, Optional, Type, TypeVar
from .base import QuerySet


__all__ = 'DTOResolver', 'DTOResolverQuerysetMixin',

T = TypeVar('T')


class DTOResolver:
    def __init__(self):
        self.registry: Dict[Type, Callable] = {}

    def has(self, dto: Type) -> bool:
        return dto in self.registry

    def add(self, dto: Type, resolver: Callable):
        if self.has(dto):
            raise ValueError(
                f'This type "{dto}" has already registered it\'s resolver'
            )

        self.registry[dto] = resolver

        return self

    def remove(self, dto: Type):
        self.registry.pop(dto, None)

    def get(self, dto: Type) -> Optional[Callable]:
        return self.registry.get(dto)

    def resolve(self, dto: Type[T], query: QuerySet, **kwargs) -> List[T]:
        if not self.has(dto):
            raise ValueError(f'No resolver registered for "{dto}" dto.')

        return self.get(dto)(query, **kwargs)


# TODO: Rework.
class DTOResolverQuerysetMixin:
    dto_resolver: DTOResolver
    dto_default_resolvers: Dict[Type, Callable] = {}

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.dto_resolver = DTOResolver()

        for datatype, resolver in self.get_dto_default_resolvers().items():
            self.dto_resolver.add(datatype, resolver)

    def get_dto_default_resolvers(self):
        return self.dto_default_resolvers

    def as_dtos(self, dto: Type[T], **kwargs) -> List[T]:
        return self.dto_resolver.resolve(dto, self, **kwargs)
