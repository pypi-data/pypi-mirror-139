from wcd_geo_db.modules.code_seeker import CodeSeeker

from .const import SOURCE


__all__ = 'OPENSTREETMAP_SEEKER',

OPENSTREETMAP_SEEKER = CodeSeeker(name=SOURCE)
