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
def slots(
        self,
        request,
        pk=None
    ):

        doctor = self.get_object()

            
        date_str = request.query_params.get(
            'date'
        )

          
        if not date_str:

            return Response(

                {
                    "status": "error",

                    "message":
                    "date query parameter is required"
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        
        try:

            selected_date = datetime.strptime(
                date_str,
                '%Y-%m-%d'
            ).date()

        except ValueError:

            return Response(

                {
                    "status": "error",

                    "message":
                    "Invalid date format"
                },

                status=status.HTTP_400_BAD_REQUEST
            )
 
        if selected_date < timezone.now().date():

            return Response(

                {
                    "status": "error",

                    "message":
                    "Past dates are not allowed"
                },

                status=status.HTTP_400_BAD_REQUEST
            )
 
        slots = generate_available_slots(
            doctor=doctor,
            date=selected_date
        )
 
        return Response(

            {
                "status": "success",

                "message":
                "Available slots retrieved successfully",

                "data": {

                    "doctor_id": doctor.id,

                    "doctor_name":
                    doctor.user.get_full_name(),

                    "date": date_str,

                    "available_slots": slots
                }
            },

            status=status.HTTP_200_OK
        )

        
        
