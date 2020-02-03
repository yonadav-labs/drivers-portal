from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from importer.models import FHVActiveDriver
from importer.serializers import RetrieveTLCNameSerializer


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