from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from importer.models import (
  FHVActiveDriver, ForHireVehicle, VehicleInsuranceInformation,
  BaseType)
from importer.serializers import (
  RetrieveTLCNameSerializer, RetrieveVINInfoFHVSerializer,
  RetrieveVINInfoInsuranceSerializer
)


class RetrieveTLCNameView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RetrieveTLCNameSerializer
    queryset = FHVActiveDriver.objects.all()

    def get_object(self):
        drivers = self.queryset.filter(license_number=self.kwargs.get('license_number'))
        attemp = self.request.query_params.get('attemp', 0)
        num_drivers = len(drivers)

        if num_drivers == 0:
            raise NotFound(detail="FHV Active Driver not found")

        return drivers[min(num_drivers, attemp)]


class RetrieveVINInfoFHVView(RetrieveAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RetrieveVINInfoFHVSerializer

  def get_queryset(self):
    return ForHireVehicle.objects.filter(
      base_number__in=BaseType.objects.all().values('base_number')
    )

  def get_object(self):
    fhv_obj = self.get_queryset().filter(
      vehicle_vin_number=self.kwargs.get('vehicle_vin_number')).first()
    
    if not fhv_obj:
      raise NotFound(detail="FHV Vehicle not found")
    return fhv_obj

  
class RetrieveVINInfoInsuranceView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = VehicleInsuranceInformation.objects.all()
    serializer_class = RetrieveVINInfoInsuranceSerializer

    def get_object(self):
      insurance = self.queryset.filter(
        vin=self.kwargs.get('vin')
      ).first()
      if not insurance:
        raise NotFound(detail="Vehicle Insurance not found")
      return insurance