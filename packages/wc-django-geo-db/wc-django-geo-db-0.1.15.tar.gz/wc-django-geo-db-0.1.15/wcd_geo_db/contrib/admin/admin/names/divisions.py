from django.contrib import admin

from wcd_geo_db.modules.names.db import DivisionName


# FIXME: Hiding before removal.
# @admin.register(DivisionName)
# class DivisionNameAdmin(admin.ModelAdmin):
#     list_display = 'id', 'name', 'level', 'country'
#     list_filter = 'level', 'country'
#     search_fields = 'name',
