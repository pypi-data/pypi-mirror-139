from wcd_geo_db.modules.code_seeker import CodeSeeker

from .const import SOURCE


__all__ = 'GEONAMES_SEEKER',

GEONAMES_SEEKER = CodeSeeker(name=SOURCE)
