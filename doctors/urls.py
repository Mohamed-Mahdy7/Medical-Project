 

from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import Specialty, DoctorProfile
from .serializers import (
    SpecialtySerializer,
    DoctorDetailSerializer
)


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Specialties:
    - list
    - retrieve
    """

    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.AllowAny]


class DoctorViewSet(viewsets.ModelViewSet):
    """
    Doctors endpoints:
    - list
    - retrieve
    - create
    - update
    - partial_update
    - destroy

    Custom endpoints:
    - /doctors/me/
    """

    queryset = DoctorProfile.objects.select_related(
        'user',
        'specialty'
    ).all()

    serializer_class = DoctorDetailSerializer

    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False,
        methods=['get'],
        url_path='me'
    )
    def me(self, request):
        """
        Return current logged-in doctor's profile
        """

        doctor = DoctorProfile.objects.filter(
            user=request.user
        ).first()

        if not doctor:
            return Response(
                {
                    "detail": "Doctor profile not found."
                },
                status=404
            )

        serializer = self.get_serializer(doctor)

        return Response(serializer.data)


router = DefaultRouter()

router.register(
    r'specialties',
    SpecialtyViewSet,
    basename='specialty'
)

router.register(
    r'doctors',
    DoctorViewSet,
    basename='doctor'
)

urlpatterns = router.urls