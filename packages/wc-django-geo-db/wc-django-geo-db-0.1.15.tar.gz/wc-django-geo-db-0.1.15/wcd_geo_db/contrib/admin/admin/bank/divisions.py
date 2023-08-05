from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from pxd_lingua.admin import TranslationsInlineAdmin
from wcd_geo_db.modules.code_seeker.admin import CodesInliner
from wcd_geo_db.modules.bank.db import (
    Division, DivisionTranslation, DivisionCode,
    DivisionPrefix, DivisionPrefixTranslation,
)


class DivisionTranslationsInlineAdmin(TranslationsInlineAdmin):
    model = DivisionTranslation


class DivisionCodeInlineAdmin(CodesInliner):
    model = DivisionCode


@admin.register(Division)
class DivisionAdmin(OSMGeoAdmin, admin.ModelAdmin):
    list_display = 'id', 'name', 'label', 'level', 'path', 'types'
    list_filter = 'level', 'prefix',
    search_fields = 'name', 'label', 'types', 'codes_set__code', 'codes_set__value'
    autocomplete_fields = 'parent',

    inlines = (
        DivisionCodeInlineAdmin, DivisionTranslationsInlineAdmin,
    )

    def save_related(self, request, form, formsets, change) -> None:
        result = super().save_related(request, form, formsets, change)

        Division.objects.filter(pk=form.instance.pk).update_json_from_relations()

        return result


@admin.register(DivisionTranslation)
class DivisionTranslationAdmin(admin.ModelAdmin):
    list_display = 'id', '__str__', 'language'
    list_filter = 'language',
    search_fields = 'name', 'synonyms', 'language'
    autocomplete_fields = 'entity',


class DivisionPrefixTranslationsInlineAdmin(TranslationsInlineAdmin):
    model = DivisionPrefixTranslation


@admin.register(DivisionPrefix)
class DivisionPrefixAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'short',
    search_fields = 'name', 'short',

    inlines = (
        DivisionPrefixTranslationsInlineAdmin,
    )
