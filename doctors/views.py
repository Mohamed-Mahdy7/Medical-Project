from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from rest_framework.response import Response
from rest_framework import viewsets
from .models import (
    Specialty, DoctorProfile
)
from .serializers import (
    SpecialtySerializer, DoctorProfileSerializer 
)   


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
class DoctorViewSet(viewsets.ModelViewSet):
     queryset= DoctorProfile.objects.all()
     serializer_class = DoctorProfileSerializer


@action(
    detail=True,
    methods=['get'],
    permission_classes=[IsAuthenticated],
    url_path='slots'
)
def slots(self, request, pk=None):
    from datetime import date as date_type, datetime
    from availability.models import Availability
    from .utils import generate_available_slots

    date_str = request.query_params.get('date')

    if not date_str:
        return Response({
            "status": "error",
            "message": "date query parameter is required. Format: YYYY-MM-DD."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({
            "status": "error",
            "message": "Invalid date format. Use YYYY-MM-DD."
        }, status=status.HTTP_400_BAD_REQUEST)

    if date < date_type.today():
        return Response({
            "status": "error",
            "message": "Cannot query slots for a past date."
        }, status=status.HTTP_400_BAD_REQUEST)

    slots = generate_available_slots(doctor_id=pk, date=date)

    return Response({
        "status": "success",
        "message": "Available slots retrieved successfully.",
        "data": {
            "doctor_id": pk,
            "date": date_str,
            "available_slots": slots
        }
    }, status=status.HTTP_200_OK)