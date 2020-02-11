try:
    ## TODO replace for orjson
    # https://pypi.org/project/orjson/
    import rapidjson as json
except ImportError:
    import json

import traceback

from celery import Task
from celery.utils.log import get_task_logger

from django.utils import dateparse

from importer.utils import create_hash
from importer.clients import (
    nyc_data_api_client_factory,
    download_xls_client_factory,
    download_fast_xls_client_factory,
)
from importer.models import (
    ImportProcessLogTask,
    MedallionDriver,
    ForHireVehicle,
    FHVActiveDriver,
    VehicleInsuranceInformation,
)
from importer.constants import (
    NYC_API_MEDALLION_DRIVERS_DATASET_ID,
    NYC_API_FOR_HIRE_VEHICLES_DATASET_ID,
    NYC_API_FHV_DRIVERS_DATASET_ID,
    NYC_XLSX_VEHICLES_INSURANCE_SOURCE,
    NYC_XLSX_VEHICLES_INSURANCE_HEADER,
    IMPORT_PROCESS_STATUS_PROCESSING,
    IMPORT_PROCESS_STATUS_DONE,
    IMPORT_PROCESS_STATUS_ERROR,
)

from stableins.celery import app


logger = get_task_logger(__name__)


class BaseImporterTask(Task):
    dataset_id_source = None
    dataset_name = None
    _client = None
    limit = 5000

    def __init__(self):
        self.import_task_object = None
        self.totals = None
        self.offset = 0
        self.parsed = 0
        self.parsed_error = 0
        self.created = 0
        self.updated = 0
        self.retrieve = 0
        self.retrieve_error = 0
        self.retrieve_error_offsets = []

    @property
    def client(self):
        if not self._client:
            logger.info("Import task: Initializing client...")
            self._client = self.initialize_client()
        return self._client

    def get_dataset_id_or_source(self):
        return self.dataset_id_source

    def initialize_client(self):
        raise NotImplementedError

    def parse_element(self, element):
        raise NotImplementedError

    def create_db_task(self):
        return ImportProcessLogTask.objects.create(
            dataset_name=self.dataset_name,
            call_args={
                "dataset_name": self.dataset_name,
                "dataset_id": self.get_dataset_id_or_source(),
                "offset": self.offset,
                "limit": self.limit,
            },
        )

    def __call__(self, *args, **kwargs):
        """In celery task this function call the run method, here you can
        set some environment variable before the run of the task"""
        task = self.create_db_task()
        kwargs.update({"import_process_log_task_id": task.id})
        super().__call__(*args, **kwargs)

    def run(self, *args, import_process_log_task_id, **kwargs):
        """ Processing and importing task main entry point """
        self.import_task_object = ImportProcessLogTask.objects.get(
            pk=import_process_log_task_id
        )
        logger.info("Starting import task: {}".format(self.import_task_object))
        try:
            self.start()
        except Exception as e:
            logger.error("Import task: {} {}".format(self.import_task_object, e))
            self.import_task_object.last_traceback = traceback.format_exc()
            self.import_task_object.process_status = IMPORT_PROCESS_STATUS_ERROR
            self.import_task_object.save()

    def start(self):
        self.totals = self.client.get_count()
        call_args = self.import_task_object.call_args
        self.limit = call_args.get("limit", self.limit)
        self.offset = call_args.get("offset", self.offset)
        self.retrieve_data()
        self.summary(end=True)
        logger.info("End import task: {}".format(self.import_task_object))

    def summary(self, end=False):
        if end:
            self.import_task_object.process_status = IMPORT_PROCESS_STATUS_DONE
        self.import_task_object.summary = {
            "offset": self.offset,
            "limit": self.limit,
            "total": self.totals,
            "parsed": self.parsed,
            "parse_errors": self.parsed_error,
            "updated": self.updated,
            "created": self.created,
            "retrieve": self.retrieve,
            "retrieve_error": self.retrieve_error,
            "retrieve_error_offsets": self.retrieve_error_offsets,
        }
        self.import_task_object.save()

    def get_next_page_offset(self):
        return self.offset + self.limit

    def get_offset_data(self):
        data = None
        try:
            data = self.client.get(self.offset, self.limit)
        except Exception:
            self.import_task_object.last_traceback = traceback.format_exc()
            self.import_task_object.save()
            self.retrieve_error_offsets.append(self.offset)
            self.retrieve_error += 1
            logger.error(
                "Import task: {} - Error retrieving offset: {}".format(
                    self.import_task_object, self.offset
                )
            )
        else:
            logger.info(
                "Import task: {} - Retrieved offset: {}".format(
                    self.import_task_object, self.offset
                )
            )
            self.retrieve += 1
        return data

    def retrieve_data(self):
        while self.offset < self.totals:
            data = self.get_offset_data()
            if data:
                self.parse_data(data)
            self.summary()
            self.offset = self.get_next_page_offset()

    def parse_data(self, data):
        for element in data:
            try:
                self.parse_element(element)
            except Exception as e:
                self.import_task_object.last_traceback = traceback.format_exc()
                self.import_task_object.save()
                self.parsed_error += 1
            else:
                self.parsed += 1


class MedallionImportTask(BaseImporterTask):
    name = "importer.tasks.medallion_import_task"
    dataset_name = "Medallion Drivers"
    dataset_id_source = NYC_API_MEDALLION_DRIVERS_DATASET_ID

    def initialize_client(self):
        return nyc_data_api_client_factory(self.get_dataset_id_or_source())

    def parse_element(self, element):
        encoded_element = json.dumps(element, sort_keys=True)
        raw_hash = create_hash(encoded_element)

        try:
            driver = MedallionDriver.objects.get(raw_hash=raw_hash)
        except MedallionDriver.DoesNotExist:
            pass
        else:
            # Hash match, information up to date
            return

        # No hash match, this is new driver or stalled data
        try:
            driver = MedallionDriver.objects.get(
                name=element["name"], license_number=element["license_number"]
            )
        except MedallionDriver.DoesNotExist:
            # No match on name this is new data
            self.create_element(element, encoded_element)
        except MedallionDriver.MultipleObjectsReturned:
            # This should not happend since search is
            # based on "unique together" fields, but is feasible to happen
            # on some rare race conditions
            logger.error(
                "MultipleObjectsReturned: search name={} license_number={}".format(
                    element["name"], element["license_number"]
                )
            )
        else:
            # There is a match data is outdatd
            self.update_element(element, encoded_element, driver)

    def create_element(self, element, encoded_element):
        expiration_date = dateparse.parse_datetime(element["expiration_date"])
        last_updated_date = dateparse.parse_datetime(element["last_updated_date"])
        last_updated_time = dateparse.parse_time(element["last_updated_time"])

        MedallionDriver.objects.create(
            **{
                "expiration_date": expiration_date.date(),
                "last_updated_date": last_updated_date.date(),
                "last_updated_time": last_updated_time,
                "license_number": element["license_number"],
                "name": element["name"],
                "type": element["type"],
                "raw": encoded_element,
            }
        )
        self.created += 1

    def update_element(self, element, encoded_element, obj):
        expiration_date = dateparse.parse_datetime(element["expiration_date"])
        last_updated_date = dateparse.parse_datetime(element["last_updated_date"])
        last_updated_time = dateparse.parse_time(element["last_updated_time"])

        obj.expiration_date = expiration_date.date()
        obj.last_updated_date = last_updated_date.date()
        obj.last_updated_time = last_updated_time
        obj.license_number = element["license_number"]
        obj.name = element["name"]
        obj.type = element["type"]
        obj.raw = encoded_element
        obj.save()
        self.updated += 1


class ForHireImportTask(BaseImporterTask):
    name = "importer.tasks.for_hire_import_task"
    dataset_name = "For Hire Vehicles (FHV)"
    dataset_id_source = NYC_API_FOR_HIRE_VEHICLES_DATASET_ID

    def initialize_client(self):
        return nyc_data_api_client_factory(self.get_dataset_id_or_source())

    def parse_element(self, element):
        encoded_element = json.dumps(element, sort_keys=True)
        raw_hash = create_hash(encoded_element)
        try:
            driver = ForHireVehicle.objects.get(raw_hash=raw_hash)
        except ForHireVehicle.DoesNotExist:
            pass
        else:
            # Hash match, information up to date
            return

        # No hash match, this is new driver or stalled data
        try:
            driver = ForHireVehicle.objects.get(
                name=element["name"],
                vehicle_license_number=element["vehicle_license_number"],
            )
        except ForHireVehicle.DoesNotExist:
            # No match on name this is new data
            self.create_element(element, encoded_element)
        except ForHireVehicle.MultipleObjectsReturned:
            # This should not happend since search is
            # based on "unique together" fields, but is feasible to happen
            # on some rare race conditions
            logger.error(
                "MultipleObjectsReturned: search name={} vehicle_license_number={}".format(
                    element["name"], element["vehicle_license_number"]
                )
            )
        else:
            # There is a match data is outdatd
            self.update_element(element, encoded_element, driver)

    def create_element(self, element, encoded_element):
        expiration_date = dateparse.parse_datetime(element.pop("expiration_date"))
        last_date_updated = dateparse.parse_datetime(element.pop("last_date_updated"))
        last_time_updated = dateparse.parse_time(element.pop("last_time_updated"))

        create_data = {
            "raw": encoded_element,
            "expiration_date": expiration_date.date(),
            "last_date_updated": last_date_updated.date(),
            "last_time_updated": last_time_updated,
        }

        certification_date = element.pop("certification_date", None)
        if certification_date:
            create_data.update(
                {"certification_date": dateparse.parse_datetime(certification_date)}
            )
        hack_up_date = element.pop("hack_up_date", None)
        if hack_up_date:
            create_data.update({"hack_up_date": dateparse.parse_datetime(hack_up_date)})

        for key, value in element.items():
            create_data.update({key: value})

        ForHireVehicle.objects.create(**create_data)
        self.created += 1

    def update_element(self, element, encoded_element, obj):
        expiration_date = dateparse.parse_datetime(element.pop("expiration_date"))
        last_date_updated = dateparse.parse_datetime(element.pop("last_date_updated"))
        last_time_updated = dateparse.parse_time(element.pop("last_time_updated"))

        obj.expiration_date = expiration_date.date()
        obj.last_date_updated = last_date_updated.date()
        obj.last_time_updated = last_time_updated
        obj.raw = encoded_element

        certification_date = element.pop("certification_date", None)
        if certification_date:
            setattr(
                obj, "certification_date", dateparse.parse_datetime(certification_date)
            )

        hack_up_date = element.pop("hack_up_date", None)
        if hack_up_date:
            setattr(obj, "hack_up_date", dateparse.parse_datetime(hack_up_date))

        for key, value in element.items():
            setattr(obj, key, value)

        obj.save()
        self.updated += 1


class VehicleInsuranceImportTask(BaseImporterTask):
    name = "importer.tasks.vehicle_insurance_import_task"
    dataset_name = "Vehicle Insurance Information"
    dataset_id_source = NYC_XLSX_VEHICLES_INSURANCE_SOURCE
    limit = 10000

    def initialize_client(self):
        return download_fast_xls_client_factory(
            self.get_dataset_id_or_source(), NYC_XLSX_VEHICLES_INSURANCE_HEADER
        )
        # return download_xls_client_factory(
        #     self.get_dataset_id_or_source(), NYC_XLSX_VEHICLES_INSURANCE_HEADER
        # )

    def parse_element(self, element):
        # encoded_element = json.dumps(element, sort_keys=True)
        encoded_element = element.to_json()
        raw_hash = create_hash(encoded_element)

        try:
            driver = VehicleInsuranceInformation.objects.get(raw_hash=raw_hash)
        except VehicleInsuranceInformation.DoesNotExist:
            pass
        else:
            # Hash match, information up to date
            return

        # No hash match, this is new data or stalled data
        try:
            driver = VehicleInsuranceInformation.objects.get(
                vin=element.vin, tlc_license_number=element.tlc_license_number
            )
        except VehicleInsuranceInformation.DoesNotExist:
            # No match on name this is new data
            self.create_element(element, encoded_element)
        except VehicleInsuranceInformation.MultipleObjectsReturned:
            # This should not happend since search is
            # based on "unique together" fields, but is feasible to happen
            # on some rare race conditions
            logger.error(
                "MultipleObjectsReturned: search vin={} tlc_license_number={}".format(
                    element.vin, element.tlc_license_number
                )
            )
            return
        else:
            # There is a match data is outdated
            self.update_element(element, encoded_element, driver)

    def create_element(self, element, encoded_element):
        create_data = {"raw": encoded_element}

        create_data.update(**element.to_dict())

        VehicleInsuranceInformation.objects.create(**create_data)
        self.created += 1

    def update_element(self, element, encoded_element, obj):
        obj.raw = encoded_element
        for key, value in element.to_dict().items():
            setattr(obj, key, value)
        obj.save()
        self.updated += 1


class FHVActiveDriverImportTask(BaseImporterTask):
    name = "importer.tasks.fhv_active_driver_import_task"
    dataset_name = "For Hire Vehicles (FHV) - Active Drivers"
    dataset_id_source = NYC_API_FHV_DRIVERS_DATASET_ID

    def initialize_client(self):
        return nyc_data_api_client_factory(self.get_dataset_id_or_source())

    def parse_element(self, element):
        encoded_element = json.dumps(element, sort_keys=True)
        raw_hash = create_hash(encoded_element)
        try:
            driver = FHVActiveDriver.objects.get(raw_hash=raw_hash)
        except FHVActiveDriver.DoesNotExist:
            pass
        else:
            # Hash match, information up to date
            return

        # No hash match, this is new driver or stalled data
        try:
            driver = FHVActiveDriver.objects.get(
                name=element["name"],
                license_number=element["license_number"],
            )
        except FHVActiveDriver.DoesNotExist:
            # No match on name this is new data
            self.create_element(element, encoded_element)
        except FHVActiveDriver.MultipleObjectsReturned:
            # This should not happend since search is
            # based on "unique together" fields, but is feasible to happen
            # on some rare race conditions
            logger.error(
                "MultipleObjectsReturned: search name={} license_number={}".format(
                    element["name"], element["license_number"]
                )
            )
        else:
            # There is a match data is outdatd
            self.update_element(element, encoded_element, driver)

    def create_element(self, element, encoded_element):
        expiration_date = dateparse.parse_datetime(element.pop("expiration_date"))
        last_date_updated = dateparse.parse_datetime(element.pop("last_date_updated"))
        last_time_updated = dateparse.parse_time(element.pop("last_time_updated"))

        create_data = {
            "raw": encoded_element,
            "expiration_date": expiration_date.date(),
            "last_date_updated": last_date_updated.date(),
            "last_time_updated": last_time_updated,
        }

        fhv_type = element.pop("type", None)
        if fhv_type:
            element['fhv_type'] = fhv_type

        for key, value in element.items():
            create_data.update({key: value})

        FHVActiveDriver.objects.create(**create_data)
        self.created += 1

    def update_element(self, element, encoded_element, obj):
        expiration_date = dateparse.parse_datetime(element.pop("expiration_date"))
        last_date_updated = dateparse.parse_datetime(element.pop("last_date_updated"))
        last_time_updated = dateparse.parse_time(element.pop("last_time_updated"))

        obj.expiration_date = expiration_date.date()
        obj.last_date_updated = last_date_updated.date()
        obj.last_time_updated = last_time_updated
        obj.raw = encoded_element

        fhv_type = element.pop("type", None)
        if fhv_type:
            setattr(obj, "fhv_type", fhv_type)

        for key, value in element.items():
            setattr(obj, key, value)

        obj.save()
        self.updated += 1

MedallionImportTask = app.register_task(MedallionImportTask())
ForHireImportTask = app.register_task(ForHireImportTask())
VehicleInsuranceImportTask = app.register_task(VehicleInsuranceImportTask())
FHVActiveDriverImportTask = app.register_task(FHVActiveDriverImportTask())