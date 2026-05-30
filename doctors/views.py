from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.utils import timezone
from datetime import datetime, date as date_type

from .models import DoctorProfile, Specialty
from .serializers import SpecialtySerializer , DoctorProfileSerializer, DoctorprofileappointmentSerializer

from appointments.models import Appointment
from appointments.permissions import IsDoctor
from .utils import generate_available_slots

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
class DoctorViewSet(viewsets.ModelViewSet):

    queryset = DoctorProfile.objects.select_related(
        "user", "specialty"
    ).all()

    serializer_class = DoctorProfileSerializer
 
    def get_permissions(self):

        permission_map = {
            "list": [AllowAny()],
            "retrieve": [AllowAny()],

            "create": [IsAuthenticated(), IsDoctor()],
            "update": [IsAuthenticated(), IsDoctor()],
            "partial_update": [IsAuthenticated(), IsDoctor()],
            "destroy": [IsAuthenticated(), IsDoctor()],

            "me": [IsAuthenticated(), IsDoctor()],
            "slots": [AllowAny()],
            "appointments": [IsAuthenticated(), IsDoctor()],
            "update_status": [IsAuthenticated(), IsDoctor()],
        }

        return permission_map.get(self.action, [IsAuthenticated()])

    @action(detail=False, methods=["get", "put"])
    def me(self, request):

        doctor = request.user.doctor_profile

        if request.method == "GET":
            serializer = self.get_serializer(doctor)
            return Response({
                "status": "success",
                "data": serializer.data
            })

        serializer = self.get_serializer(
            doctor,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["get"])
    def slots(self, request, pk=None):

        doctor = self.get_object()

        date_str = request.query_params.get("date")

        if not date_str:
            return Response({
                "status": "error",
                "message": "date is required (YYYY-MM-DD)"
            }, status=400)

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({
                "status": "error",
                "message": "Invalid date format"
            }, status=400)

        if target_date < date_type.today():
            return Response({
                "status": "error",
                "message": "Cannot use past date"
            }, status=400)

        slots = generate_available_slots(
            doctor_id=doctor.id,
            date=target_date
        )

        return Response({
            "status": "success",
            "data": {
                "doctor_id": doctor.id,
                "date": date_str,
                "available_slots": slots
            }
        })
 
    @action(detail=False, methods=["get"])
    def appointments(self, request):

        doctor = request.user.doctor_profile

        status_filter = request.query_params.get("status")

        qs = Appointment.objects.filter(doctor=doctor)

        if status_filter:
            qs = qs.filter(status=status_filter)

        
        appointment_type = request.query_params.get("type")

        today = timezone.now().date()

        if appointment_type == "upcoming":
            qs = qs.filter(date__gte=today)

        elif appointment_type == "past":
            qs = qs.filter(date__lt=today)
        serializer = DoctorprofileappointmentSerializer(qs, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        })
 
    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):

        doctor = request.user.doctor_profile

        try:
            appointment = Appointment.objects.get(
                id=pk,
                doctor=doctor
            )
        except Appointment.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Appointment not found"
            }, status=404)

        new_status = request.data.get("status")

        if new_status not in ["CONFIRMED", "REJECTED"]:
            return Response({
                "status": "error",
                "message": "Invalid status"
            }, status=400)

        appointment.status = new_status
        appointment.notes = request.data.get("notes", appointment.notes)
        appointment.save()
         

        return Response({
            "status": "success",
            "message": "Status updated successfully"
        })







































































 