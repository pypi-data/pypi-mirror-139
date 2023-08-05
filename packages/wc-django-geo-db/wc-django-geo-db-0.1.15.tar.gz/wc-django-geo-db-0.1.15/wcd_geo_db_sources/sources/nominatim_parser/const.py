from django.utils.translation import pgettext_lazy
from django.db import models

from .._base import BaseImportStage as B


__all__ = 'SOURCE', 'ImportStage'

SOURCE = 'NOMINATIM'


class ImportStage(models.TextChoices):
    INITIAL = B.INITIAL.value, B.INITIAL.label
    # UPLOADING = '002000-uploading', pgettext_lazy('wcd_geo_db_sources:source', 'Uploading')
    PARSING = B.PARSING.value, B.PARSING.label
    MERGE = B.MERGE.value, B.MERGE.label
    MERGE_TRANSLATIONS = B.MERGE_TRANSLATIONS.value, B.MERGE_TRANSLATIONS.label
    CLEANUP = B.CLEANUP.value, B.CLEANUP.label
