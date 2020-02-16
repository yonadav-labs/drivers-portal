from django.contrib import admin

from importer.models import (
    VehicleInsuranceInformation,
    MedallionDriver,
    ForHireVehicle,
    FHVActiveDriver,
    ImportProcessLogTask,
    BaseType
)


class VehicleInsuranceInformationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tlc_license_number",
        "automobile_insurance_name",
        "automobile_insurance_code",
        "modified",
    )
    readonly_fields = ("raw", "created", "modified", "raw_hash")
    search_fields = (
        "tlc_license_number",
        "automobile_insurance_name",
        "automobile_insurance_code",
        "automobile_insurance_policy_number",
        "id",
    )
    ordering = ("-created",)


class MedallionDriverAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "license_number", "modified")
    readonly_fields = ("raw", "created", "modified", "raw_hash")
    search_fields = ("name", "license_number", "id")


class ForHireVehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "dmv_license_plate_number", "modified")
    readonly_fields = ("raw", "created", "modified", "raw_hash")
    search_fields = ("name", "dmv_license_plate_number", "base_number", "id")


class ImportProcessLogTaskAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created",
        "process_status",
        "display_percentage",
        "display_total",
        "display_parsed",
        "dataset_name",
    )
    readonly_fields = (
        "process_status",
        "created",
        "modified",
        "dataset_name",
        "summary",
        "call_args",
        "last_traceback",
    )
    ordering = ("-created", "-modified", "process_status")


class FHVActiveDriverAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "license_number", "modified")
    readonly_fields = ("raw", "created", "modified", "raw_hash")
    search_fields = ("name", "license_number", "id")


admin.site.register(VehicleInsuranceInformation, VehicleInsuranceInformationAdmin)
admin.site.register(MedallionDriver, MedallionDriverAdmin)
admin.site.register(ForHireVehicle, ForHireVehicleAdmin)
admin.site.register(FHVActiveDriver, FHVActiveDriverAdmin)
admin.site.register(ImportProcessLogTask, ImportProcessLogTaskAdmin)
admin.site.register(BaseType)