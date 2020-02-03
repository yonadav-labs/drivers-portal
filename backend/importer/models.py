from django.db import models
from django.contrib.postgres.fields import JSONField

from base.models import BaseModel

from importer.mixins import HashedRawMixin
from importer.constants import (
    IMPORT_PROCESS_STATUS_CHOICES, IMPORT_PROCESS_STATUS_PROCESSING)

# TODO: Add a manager to query by indexed fields

class VehicleInsuranceInformation(HashedRawMixin, BaseModel):
    """
    Vehicle Insurance Information
    """
    # https://www1.nyc.gov/assets/tlc/downloads/datasets/current_insurance.xlsx
    class Meta:
        verbose_name = "Vehicle Insurance Information"
        verbose_name_plural = "Vehicles Insurance Information"
        indexes = [
            models.Index(fields=["vin", "tlc_license_number", ]),
        ]

    # ---- Custom Fields
    raw = JSONField(
        verbose_name="Raw data"
    )
    # ---- API Fields
    tlc_license_type = models.CharField(
        verbose_name="TLC License type",
        max_length=511,
        blank=False,
        null=False
    )
    tlc_license_number = models.CharField(
        verbose_name="TLC License number",
        max_length=511,
        blank=False,
        null=False
    )
    dmv_plate = models.CharField(
        verbose_name="DMV plate",
        max_length=511,
        blank=False,
        null=False
    )
    vin = models.CharField(
        verbose_name="VIN",
        max_length=511,
        blank=False,
        null=False
    )
    automobile_insurance_code = models.CharField(
        verbose_name="Automobile insurance code",
        max_length=511,
        blank=False,
        null=False
    )
    automobile_insurance_name = models.CharField(
        verbose_name="Automobile insurance name",
        max_length=511,
        blank=False,
        null=False
    )
    automobile_insurance_policy_number = models.CharField(
        verbose_name="Automobile insurance policy number",
        max_length=511,
        blank=False,
        null=False
    )
    vehicle_owner_name = models.CharField(
        verbose_name="Vehicle owner name",
        max_length=511,
        blank=False,
        null=False
    )
    affiliated_base_or_taxi_agent_or_fleet_license_number = models.CharField(
        verbose_name="Affiliated base or taxi agent or fleet license number",
        max_length=511,
        blank=False,
        null=False
    )

    def __str__(self):
        return "VehicleInsurance-{}".format(self.id)


class MedallionDriver(HashedRawMixin, BaseModel):
    """
    Medallion Drivers
    """
    # https://dev.socrata.com/foundry/data.cityofnewyork.us/jb3k-j3gp
    class Meta:
        verbose_name = "Medallion Drivers"
        verbose_name_plural = "Medallion Drivers"
        indexes = [
            models.Index(fields=["name", "license_number", ]),
        ]

    # ---- Custom Fields
    raw = JSONField(
        verbose_name="Raw data"
    )
    # ---- API Fields
    expiration_date = models.DateField(
        verbose_name="Expiration date",
        auto_now_add=False,
        auto_now=False
    )
    last_updated_date = models.DateField(
        verbose_name="Last updated date",
        auto_now_add=False,
        auto_now=False
    )
    last_updated_time = models.TimeField(
        verbose_name="Last updated time",
        auto_now_add=False,
        auto_now=False
    )
    license_number = models.CharField(
        verbose_name="License number",
        max_length=511,
        blank=False,
        null=False
    )
    name = models.CharField(
        verbose_name="Name",
        max_length=511,
        blank=False,
        null=False
    )
    type = models.CharField(
        verbose_name="Type",
        max_length=511,
        blank=False,
        null=False
    )

    def __str__(self):
        return "Driver-{}".format(self.id)


class ForHireVehicle(HashedRawMixin, BaseModel):
    """
    For Hire Vehicle (FHV)
    """
    class Meta:
        verbose_name = "For Hire Vehicle"
        verbose_name_plural = "For Hire Vehicles"
        indexes = [
            models.Index(fields=["name", "vehicle_license_number", ]),
        ]

    # ---- Custom Fields
    raw = JSONField(
        verbose_name="Raw data"
    )
    # ---- API Fields
    active = models.CharField(
        verbose_name="Active",
        max_length=511,
        blank=False,
        null=False
    )
    base_address = models.CharField(
        verbose_name="Base address",
        max_length=511,
        blank=False,
        null=False
    )
    base_name = models.CharField(
        verbose_name="Base name",
        max_length=511,
        blank=False,
        null=False
    )
    base_number = models.CharField(
        verbose_name="Base number",
        max_length=511,
        blank=False,
        null=False
    )
    base_telephone_number = models.CharField(
        verbose_name="Base telephone number",
        max_length=511,
        blank=False,
        null=False
    )
    base_type = models.CharField(
        verbose_name="Base type",
        max_length=511,
        blank=False,
        null=False
    )
    dmv_license_plate_number = models.CharField(
        verbose_name="DMV license plate number",
        max_length=511,
        blank=False,
        null=False
    )
    permit_license_number = models.CharField(
        verbose_name="Permit license number",
        max_length=511,
        blank=True,
        null=True
    )
    license_type = models.CharField(
        verbose_name="License type",
        max_length=511,
        blank=False,
        null=False
    )
    name = models.CharField(
        verbose_name="Name",
        max_length=511,
        blank=False,
        null=False
    )
    reason = models.CharField(
        verbose_name="Reason",
        max_length=511,
        blank=False,
        null=False
    )
    vehicle_license_number = models.CharField(
        verbose_name="Vehicle license number",
        max_length=511,
        blank=False,
        null=False
    )
    vehicle_vin_number = models.CharField(
        verbose_name="Vehicle VIN number",
        max_length=511,
        blank=False,
        null=False
    )
    vehicle_year = models.PositiveIntegerField(
        verbose_name="Vehicle year"
    )
    website = models.CharField(
        verbose_name="Website",
        max_length=511,
        blank=True,
        null=False
    )
    wheelchair_accessible = models.CharField(
        verbose_name="Wheelchair accessible",
        max_length=511,
        blank=True,
        null=True
    )
    veh = models.CharField(
        verbose_name="VEH",
        max_length=511,
        blank=True,
        null=True
    )
    certification_date = models.DateField(
        verbose_name="Certification date",
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    hack_up_date = models.DateField(
        verbose_name="Hack up date",
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    expiration_date = models.DateField(
        verbose_name="Expiration date",
        auto_now_add=False,
        auto_now=False
    )
    last_date_updated = models.DateField(
        verbose_name="Last date updated",
        auto_now_add=False,
        auto_now=False
    )
    last_time_updated = models.TimeField(
        verbose_name="Last time updated",
        auto_now_add=False,
        auto_now=False
    )

    def __str__(self):
        return "FHV-{}".format(self.id)

class FHVActiveDriver(HashedRawMixin, BaseModel):
    """
    For Hire Vehicle (FHV) Active Driver
    https://data.cityofnewyork.us/resource/xjfq-wh2d.json
    """
    class Meta:
        verbose_name = "FHV Active Driver"
        verbose_name_plural = "FHV Active Drivers"
        indexes = [
            models.Index(fields=["license_number", ]),
            models.Index(fields=["name", "license_number", ]),
        ]

    # ---- Custom Fields
    raw = JSONField(
        verbose_name="Raw data"
    )
    # ---- API Fields

    license_number = models.CharField(
        verbose_name="License number",
        max_length=511,
        blank=False,
        null=False
    )
    name = models.CharField(
        verbose_name="Name",
        max_length=511,
        blank=False,
        null=False
    )
    # type = fhv_type
    fhv_type = models.CharField(
        verbose_name="Type",
        max_length=511,
        blank=False,
        null=False
    )
    wheelchair_accessible_trained = models.CharField(
        verbose_name="Wheelchair Accesible Trained",
        max_length=511,
        blank=False,
        null=False
    )
    expiration_date = models.DateField(
        verbose_name="Expiration date",
        auto_now_add=False,
        auto_now=False
    )
    last_date_updated = models.DateField(
        verbose_name="Last date updated",
        auto_now_add=False,
        auto_now=False
    )
    last_time_updated = models.TimeField(
        verbose_name="Last time updated",
        auto_now_add=False,
        auto_now=False
    )

    def __str__(self):
        return "FHV Active Driver-{}".format(self.id)


class ImportProcessLogTask(BaseModel):
    class Meta:
        verbose_name = "Import process log task"
        verbose_name_plural = "Import process log tasks"

    process_status = models.CharField(
        max_length=100,
        choices=IMPORT_PROCESS_STATUS_CHOICES,
        default=IMPORT_PROCESS_STATUS_PROCESSING
    )
    dataset_name = models.CharField(
        verbose_name="Dataset name",
        max_length=511
    )
    summary = JSONField(
        verbose_name="Summary",
        default=dict
    )
    call_args = JSONField(
        verbose_name="Call args",
        default=dict
    )
    last_traceback = models.TextField(
        verbose_name="Last Traceback",
        default='',
        null=True
    )

    def display_total(self):
        if not self.summary or len(self.summary) == 0:
            return "??"
        return self.summary.get("total", "??")
    display_total.short_description = 'Total'

    def display_parsed(self):
        if not self.summary or len(self.summary) == 0:
            return "??"
        return self.summary.get("parsed", "??")
    display_parsed.short_description = 'Parsed'

    def display_percentage(self):
        if not self.summary or len(self.summary) == 0:
            return "??%"
        _total = self.summary.get("total", None)

        if not _total:
            return "??%"

        return "{}%".format(
            int((self.summary.get("parsed", 0) / _total) * 100
            )
        )
    display_percentage.short_description = 'Percentage'

    def __str__(self):
        return "Import task-{}-{}".format(self.id, self.dataset_name)
