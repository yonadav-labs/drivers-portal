import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings 

from importer.constants import BASE_TYPE_BLACKCAR, BASE_TYPE_LIVERY
from importer.models import BaseType

from importer.tasks import (
    MedallionImportTask,
    ForHireImportTask,
    VehicleInsuranceImportTask,
    FHVActiveDriverImportTask
)


class Command(BaseCommand):
    help = (
        "Load base types from file"
    )

    def handle(self, *args, **options):
      path = os.path.join(
        settings.BASE_DIR,
        "importer",
        "docs",
        "base_types.csv"
      )
      created_count = 0
      updated_count = 0

      with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        first_line = True
        for row in spamreader:
          if first_line:
            first_line = False
            continue
          
          _, created = BaseType.objects.update_or_create(
            base_number=row[0].strip(),
            defaults={
              'base_name': row[1].strip(),
              'base_type': BASE_TYPE_LIVERY if row[2].strip() == 'Livery' else BASE_TYPE_BLACKCAR,
              'luxury_discount': row[3].strip() == 'Y',
              'loss_control_discount': row[4].strip() == 'Y',
            }
          )
          if created:
            created_count += 1
          else:
            updated_count += 1
      print(f"Created {created_count} base types")
      print(f"Updated {updated_count} base types")