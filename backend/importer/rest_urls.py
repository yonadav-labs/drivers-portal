from django.urls import path

from importer.rest_views import (
  RetrieveTLCNameView, RetrieveVINInfoFHVView, RetrieveVINInfoInsuranceView
)

urlpatterns = [
    path('fhv_driver/<license_number>/', RetrieveTLCNameView.as_view(), name="retrieve-tlc"),
    path('for_hire_vehicle/<vehicle_vin_number>/', RetrieveVINInfoFHVView.as_view(), name="retrieve-fhv"),
    path('vehicle_insurance_information/<vin>/', RetrieveVINInfoInsuranceView.as_view(), name="retrieve-insurance"),
]