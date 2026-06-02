from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from datetime import datetime, date as date_type
from .models import Specialty, DoctorProfile
from .serializers import SpecialtySerializer, DoctorProfileSerializer
from .utils import generate_available_slots


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

    @action(
    detail=False,
    methods=['get', 'put'],
    permission_classes=[IsAuthenticated],
    url_path="me",
    )
    def me(self, request):
        print("request.user:", request.user)
        print("Doctor Profile:", request.user.doctor_profile)
        print("Profile User:", request.user.doctor_profile.user)
        serializer=DoctorProfileSerializer(request.user.doctor_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
    detail=True,
    methods=['get'],
    permission_classes=[IsAuthenticated],
    url_path='slots'
    )
    def slots(self, request, pk=None):

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

        slots, slot_duration = generate_available_slots(doctor_id=pk, date=date)

        return Response({
            "status": "success",
            "message": "Available slots retrieved successfully.",
            "data": {
                "doctor_id": pk,
                "date": date_str,
                "available_slots": slots,
                "slot_duration_minutes": slot_duration
            }
        }, status=status.HTTP_200_OK)
