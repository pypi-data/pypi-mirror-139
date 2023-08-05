from django.conf import settings

if 'wcd_geo_db.contrib.admin' in settings.INSTALLED_APPS:
    from . import bank
