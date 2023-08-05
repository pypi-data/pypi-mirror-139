from wcd_geo_db.modules.code_seeker import CodeSeeker

from .const import SOURCE


__all__ = 'POSTCODE_SEEKER',

POSTCODE_SEEKER = CodeSeeker(name=SOURCE)
"""FIXME: Postcodes will duplicate. Be careful."""
