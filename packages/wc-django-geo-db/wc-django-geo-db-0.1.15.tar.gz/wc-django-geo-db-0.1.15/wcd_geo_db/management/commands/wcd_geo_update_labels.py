from pprint import pprint
import re
from unidecode import unidecode
from django.db import models
from django.utils.text import slugify
from django.core.management.base import BaseCommand
from wcd_geo_db.modules.bank.db import Division


NUM_MATCHER = re.compile(r'^.*(-[0-9]+)$')


def make_labels(queryset):
    items = queryset.values_list('id', 'name')
    result = [
        Division(id=id, label=slugify(unidecode(name).lower()))
        for id, name in items
    ]
    Division.objects.bulk_update(
        result, fields=('label',), batch_size=500,
    )

    return len(result)


def make_labels_unique():
    items = (
        Division.objects.filter(label__in=(
            Division.objects
            .values('label')
            .annotate(count=models.Count('label'))
            .order_by('label')
            .values('label')
            .filter(count__gt=1)
        ))
        .values_list('id', 'label', 'parent__label', 'path__depth')
        .order_by('label', 'path__depth')
    )

    result = []
    count = 0
    labled = 0
    last = None

    for id, label, plabel, *_ in items:
        if last != label:
            count = 0
            labled = 0

        count += 1
        last = label

        if count == 1:
            continue

        pl, *_ = plabel.split('-')

        if pl and not (pl in label):
            label = label + '-' + pl
            labled += 1
        else:
            # FIXME: Counters should not be done multiple times.
            if NUM_MATCHER.match(label) is not None:
                print('Number resolver used couple times:')
                print((id, label))
                continue

            if pl != label and label.endswith('-' + pl):
                label = label[:0 - (len(pl) + 1)]

            label = label + '-' + str(count - labled)

        result.append(Division(id=id, label=label.replace('--', '-')))

    Division.objects.bulk_update(
        result, fields=('label',), batch_size=500,
    )

    return len(result)


class Command(BaseCommand):
    help = 'Runs label generation for all divisions.'

    def add_arguments(self, parser):
        parser.add_argument('--all', nargs=1, type=bool, default=False)

    def handle(self, *args, **options):
        queryset = Division.objects.all() if options['all'] else (
            Division.objects.filter(label='')
        )

        labels = make_labels(queryset)

        print(f'Generated {labels} new labels.')

        deduplicates = make_labels_unique()

        print(f'Deduplicated {deduplicates} labels.')