from .models import Availability
from .serializers import AvailabilitySerializer

from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.
class AvailabilityViewSet(viewsets.ViewSet):
    def list(self, request):
        availabilities = Availability.objects.all()
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)