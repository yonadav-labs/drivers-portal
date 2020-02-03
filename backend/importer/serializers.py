from rest_framework import serializers

from importer.models import (
    ForHireVehicle, MedallionDriver, VehicleInsuranceInformation,
    FHVActiveDriver)


class VehicleInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleInsuranceInformation
        fields = (
            "id",
            "tlc_license_type",
            "tlc_license_number",
            "dmv_plate",
            "vin",
            "automobile_insurance_code",
            "automobile_insurance_name",
            "automobile_insurance_policy_number",
            "vehicle_owner_name",
            "affiliated_base_or_taxi_agent_or_fleet_license_number",
        )


class MedallionDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedallionDriver
        fields = (
            "id",
            "name",
            "expiration_date",
            "last_updated_date",
            "last_updated_time",
            "license_number",
            "type",
        )


class ForHireVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForHireVehicle
        fields = (
            "id",
            "active",
            "base_address",
            "base_name",
            "base_number",
            "base_telephone_number",
            "base_type",
            "dmv_license_plate_number",
            "permit_license_number",
            "license_type",
            "name",
            "reason",
            "vehicle_license_number",
            "vehicle_vin_number",
            "vehicle_year",
            "website",
            "wheelchair_accessible",
            "veh",
            "certification_date",
            "hack_up_date",
            "expiration_date",
            "last_date_updated",
            "last_time_updated",
        )

class RetrieveTLCNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    license_number = serializers.CharField(read_only=True)

    class Meta:
        model = FHVActiveDriver
        fields = (
            'license_number', 'name',
        )