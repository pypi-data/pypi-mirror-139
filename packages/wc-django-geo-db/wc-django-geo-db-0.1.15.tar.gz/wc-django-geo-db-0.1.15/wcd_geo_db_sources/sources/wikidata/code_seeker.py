from wcd_geo_db.modules.code_seeker import CodeSeeker

from .const import SOURCE


__all__ = 'WIKIDATA_SEEKER',

WIKIDATA_SEEKER = CodeSeeker(name=SOURCE)
