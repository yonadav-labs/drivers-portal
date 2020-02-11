from django.core.management.base import BaseCommand

from importer.tasks import (
    MedallionImportTask,
    ForHireImportTask,
    VehicleInsuranceImportTask,
    FHVActiveDriverImportTask
)


class Command(BaseCommand):

    help = (
        "Starts a celery task to import data from NYC Open data api and"
        "loads it into database"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--type",
            type=str,
            dest="import_type",
            choices=["fhv_drivers", "drivers", "vehicles", "insurances"],
            default="drivers",
            help='"fhv_drivers", "drivers" or "vehicles" or "insurances"',
        )
        parser.add_argument(
            "-f",
            "--flush",
            action='store_true',
            dest="flush",
            help="Flush imported data",
        )

    def handle(self, *args, **options):
        if options.get('flush'):
            from importer.models import (
                ImportProcessLogTask,
                MedallionDriver,
                ForHireVehicle,
                VehicleInsuranceInformation,
                FHVActiveDriver
            )
            ImportProcessLogTask.objects.all().delete()
            MedallionDriver.objects.all().delete()
            ForHireVehicle.objects.all().delete()
            VehicleInsuranceInformation.objects.all().delete()
            FHVActiveDriver.objects.all().delete()
            return

        import_type = options.get("import_type")
        if import_type == "fhv_drivers":
            FHVActiveDriverImportTask.delay()
            self.stdout.write("Launching FHV Active Drivers importer task")
        elif import_type == "drivers":
            MedallionImportTask.delay()
            self.stdout.write("Launching Medallion importer task")
        elif import_type == "vehicles":
            ForHireImportTask.delay()
            self.stdout.write("Launching FHV importer task")
        elif import_type == "insurances":
            VehicleInsuranceImportTask.delay()
            self.stdout.write("Launching Vehicles Insurance importer task")
        else:
            self.stdout.write("Launching nothing")
        self.stdout.write("Done")

