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
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    
