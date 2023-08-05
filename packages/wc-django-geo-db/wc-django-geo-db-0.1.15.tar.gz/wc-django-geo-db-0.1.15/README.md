# WebCase Geographical database

## Installation

```sh
pip install wc-django-geo-db
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'pxd_lingua',

  'pxd_postgres',
  'pxd_postgres.ltree',

  'wcd_geo_db',
  'wcd_geo_db.contrib.admin',
  'wcd_geo_db_sources',
]

WCD_GEO_DBSOURCES = {
  'SOURCE_IMPORT_RUNNERS': (
    'wcd_geo_db_sources.sources.katottg.process.KATOTTGImportRunner',
    'wcd_geo_db_sources.sources.katottg_to_koatuu.process.KATOTTG_TO_KOATUUImportRunner',
  )
}
```

## Usage

```python
from wcd_geo_db.client import GeoClient
from wcd_geo_db.conf import Settings
from wcd_geo_db.modules.code_seeker import registry
from wcd_geo_db_sources.sources.koatuu import KOATUU_SEEKER
from wcd_geo_db_sources.sources.katottg import KATOTTG_SEEKER
from wcd_geo_db_sources.sources.novaposhta import NOVAPOSHTA_SEEKER


client = GeoClient(settings=Settings(), code_seeker_registry=registry)

registry.register(KOATUU_SEEKER)
registry.register(KATOTTG_SEEKER)
registry.register(NOVAPOSHTA_SEEKER)

client.bank.divisions.get(ids=(1,))

found = client.bank.divisions.find(levels=(DivisionLevel.ADMINISTRATIVE_LEVEL_1,))

descendants = client.bank.divisions.find_descendants(ids=found)

# Since [0.1.15].
# Divisions can be search by `label` field now.
# Label is a sluggified version of `name` field. Unique, but there is no
# constraint on that.
client.bank.divisions.find(labels=('odesa',))
```

### Different DTOs to resolve

**Since [`0.1.15`].**

You may now choose in what variation you can retrieve your data.

There is only 2 options right now:

- as `DivisionDTO` - It's simple, but provide all the data you need for regular use. Used by default.
- as `ExtendedDivisionDTO` - Provides additional geography info(location, polygon) and prefix name definition.

```python
from wcd_geo_db.modules.bank.dtos import DivisionDTO, ExtendedDivisionDTO

# ...
# Will result in List[DivisionDTO].
client.bank.divisions.get(ids=(1,))
# Same as before: List[DivisionDTO].
client.bank.divisions.get(ids=(1,), as_dto=DivisionDTO)

# Here result changes: List[ExtendedDivisionDTO].
client.bank.divisions.get(ids=(1,), as_dto=ExtendedDivisionDTO)
```

**TODO:** Make DTO resolvers extend API to be public.

### Address formatter

```python
address = client.addresses.formatter.format_addresses(
  (
    # Sequence of address definitions.
    {
      # There could be either identifiers or DivisionDTOs in a list.
      'divisions_path': [1, 2],
      # Or you can pass a division identifer or DivisionDTO as single.
      'division': 2,
      # If both `divisions_path` and `division` will be passed - `divisions_path`
      # field will be used to get address information.
    },
  ),
  # Main language to use for formatting.
  'en',
  # Languages to use if there's no default one
  fallback_languages=('es', 'jp')
)

print(address.formatted_address)
# > 'Administrative division level 1, Country name'
```

**Since [`0.1.15`].** Added translatable division name prefixes, that now can will be used in address formatting.

### Searching

```python
search = client.bank.divisions.find(search_query={
  'query': 'Santa Monica',
  'language': 'en',
})

print(search)
# Search results will be ordered by relevance rank.
# > [438, 335. 425]
```

**Since [`0.1.12`].** Added `use_simple_search` parameter to divisions search. It forces search mechanics to use simple `__icontains` instead of trigram similarity. Query will run faster but response wouldn't be ordered by search matching relevance:

```python
search = client.bank.divisions.find(search_query={
  'query': 'Santa Monica',
  'use_simple_search': True,
  'language': 'en',
})
```

## Contrib


### [DAL](https://pypi.org/project/django-autocomplete-light/)

**Since [`0.1.12`].**

To use django autocomplete light you need to install library with `[dal]` extras.

Like so:

```sh
pip install wc-django-geo-db[dal]
```

#### Urls

Default autocomplete urls could be made as:

```python
# Importing url factory.
from wcd_geo_db.contrib.dal.urls import make_urlpatterns

# Importing defined GeoClient instance somewhere from your project:
from your_project.geo_client import client

urlpatterns = [
  # And including newly made urlpatterns into yours.
  path('', include(make_urlpatterns(client))),
]
```

Namespace for all autocomplete url is `'wcd-geo-db:dal:admin:autocomplete'`.

So for example divisions autocomplete url looks like: `'wcd-geo-db:dal:admin:autocomplete:divisions'`.

There are custom url makers also available:

```python
from django.urls import path, include

from wcd_geo_db.const import DivisionLevel
from wcd_geo_db.contrib.dal.urls import make_urlpatterns, make_divisions_path, autocomplete_namespace
from wcd_geo_db.contrib.dal.views import DivisionDalViewAdmin

from your_project.geo_client import client

urlpatterns = [
  # URLs may be extended, all of them are going to be under the same
  # autocomplete namespace.
  path('', include(make_urlpatterns(
    client,
    # For example you want to add url that displays only localities,
    # not all divisions.
    # It may be just a custom path, but we already have a generator, so use it:
    make_divisions_path(
      # Name for url.
      'localities',
      # Client also must be provided.
      client,
      # This is just kwargs for divisions.find() method.
      find_parameters={'levels': [DivisionLevel.LOCALITY]},
      # cls attribute may be omitted, but by default it's a view with no
      # access restriction. But since this is admin view we must use an
      # appropriated.
      # This could be any custom view, of course.
      cls=DivisionDalViewAdmin
    )
  ))),
]
```

After this you can use your new autocompletetion urls anywhere. For example above url name will be: `'wcd-geo-db:dal:admin:autocomplete:localities'`.

#### Admin integration

To use autocomplete urls in admin you may do something like this:

`your_application/admin.py`
```python
from dal_select2.widgets import ModelSelect2Multiple
from wcd_geo_db.contrib.dal.djhacker import formfield
from wcd_geo_db.contrib.dal.forms import PreparableModelMultipleChoiceField
from wcd_geo_db.contrib.dal.preparators import DivisionsPreparator

from your_project.geo_client import client

from .models import YourCustomModel

# With help of `djhacker` you wouldn't need to manually override formfields
# without creating custom forms for that:
formfield(
  # URL name to autocomplete divisions:
  'wcd-geo-db:dal:admin:autocomplete:divisions',
  # Your model field to patch:
  YourCustomModel.division_singular_field,
  # Special data resolver for divisions data that formats divisions
  # as addresses.
  preparator=DivisionsPreparator(
    client=client.bank.divisions,
    formatter_client=client.addresses.formatter,
  )
)

formfield(
  'wcd-geo-db:dal:admin:autocomplete:localities',
  YourCustomModel.divisions_many_to_many_field,
  preparator=DivisionsPreparator(
    client=client.bank.divisions,
    formatter_client=client.addresses.formatter,
  ),
  # Same as above, but since this is a many-to-many field there have to
  # be some adjustments made:
  # Many to many field class, that uses preparator to display selected values:
  field_class=PreparableModelMultipleChoiceField,
  # Widget to display multiselect:
  widget_class=ModelSelect2Multiple,
)
```
