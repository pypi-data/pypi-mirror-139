from django.contrib import admin
from django.utils.translation import pgettext_lazy
from wcd_geo_db.contrib.admin.admin.bank.divisions import (
    DivisionAdmin as BaseDivisionAdmin
)
from wcd_geo_db.modules.bank.db import (
    Division, DivisionTranslation, Place, Route
)
from pxd_postgres.ltree.value import LtreeValue
from wcd_geo_db.contrib.dal.djhacker import formfield
from wcd_geo_db.contrib.dal.preparators import DivisionsPreparator
from dal_admin_filters import AutocompleteFilter

from .client import client


formfield(
    'wcd-geo-db:dal:admin:autocomplete:divisions',
    Division.parent,
    preparator=DivisionsPreparator(
        client=client.bank.divisions,
        formatter_client=client.addresses.formatter,
    )
)
formfield(
    'wcd-geo-db:dal:admin:autocomplete:divisions',
    DivisionTranslation.entity,
    preparator=DivisionsPreparator(
        client=client.bank.divisions,
        formatter_client=client.addresses.formatter,
    )
)
formfield(
    'wcd-geo-db:dal:admin:autocomplete:divisions',
    Place.division,
    preparator=DivisionsPreparator(
        client=client.bank.divisions,
        formatter_client=client.addresses.formatter,
    )
)
formfield(
    'wcd-geo-db:dal:admin:autocomplete:divisions',
    Route.division,
    preparator=DivisionsPreparator(
        client=client.bank.divisions,
        formatter_client=client.addresses.formatter,
    )
)
admin.site.unregister(Division)


class ParentDivisionFilter(AutocompleteFilter):
    title = pgettext_lazy('wcd_geo_db', 'Divisions parent filter')
    field_name = 'parent'
    autocomplete_url = 'wcd-geo-db:dal:admin:autocomplete:divisions'


class AncestorDivisionFilter(AutocompleteFilter):
    title = pgettext_lazy('wcd_geo_db', 'Divisions Ancestor filter')
    field_name = 'ancestor'
    use_pk_exact = False
    autocomplete_url = 'wcd-geo-db:dal:admin:autocomplete:divisions'

    def get_queryset_for_field(self, model, name):
        return Division.parent.get_queryset()

    def queryset(self, request, queryset):
        v = self.value()

        if v:
            return queryset.filter(path__match=f'*.{v}.*')
        else:
            return queryset


@admin.register(Division)
class DivisionAdmin(BaseDivisionAdmin):
    list_filter = (
        'level',
        'prefix',
        AncestorDivisionFilter,
        ParentDivisionFilter,
    )
