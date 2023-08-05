from pxd_lingua import create_translated_model

from .divisions import Division, DivisionPrefix


__all__ = 'DivisionTranslation', 'DivisionPrefixTranslation',


DivisionTranslation = create_translated_model(
    Division, fields=('name', 'synonyms')
)
DivisionPrefixTranslation = create_translated_model(
    DivisionPrefix, fields=('name', 'short')
)
