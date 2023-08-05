from wcd_geo_db.client import GeoClient
from wcd_geo_db.conf import Settings
from wcd_geo_db.modules.code_seeker import registry

client = GeoClient(settings=Settings(), code_seeker_registry=registry)
