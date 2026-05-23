from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)

from .models import (
    Specialty,
    DoctorProfile
)

from .serializers import (
    SpecialtySerializer,
    DoctorListSerializer,
    DoctorDetailSerializer,
    DoctorCreateUpdateSerializer
)
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView

class SpecialtyListView(ListAPIView):

    queryset = Specialty.objects.all()

    serializer_class = SpecialtySerializer

    permission_classes = [AllowAny]


class DoctorListView(ListAPIView):

    serializer_class = DoctorListSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):

        queryset = DoctorProfile.objects.select_related(
            'user',
            'specialty'
        ).filter(
            is_approved=True,
            is_blocked=False
        )

        specialty = self.request.query_params.get(
            'specialty'
        )

        if specialty:

            queryset = queryset.filter(
                specialty__id=specialty
            )

        name = self.request.query_params.get(
            'name'
        )

        if name:

            queryset = queryset.filter(
                user__first_name__icontains=name
            )

        return queryset


class DoctorDetailView(RetrieveAPIView):

    queryset = DoctorProfile.objects.select_related(
        'user',
        'specialty'
    )

    serializer_class = DoctorDetailSerializer

    permission_classes = [AllowAny]


class DoctorMeView(RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.request.method == 'GET':

            return DoctorDetailSerializer

        return DoctorCreateUpdateSerializer

    def get_object(self):

        return self.request.user.doctor_profile
    

 

class DoctorDeleteView(DestroyAPIView):

    queryset = DoctorProfile.objects.all()

    serializer_class = DoctorDetailSerializer

    permission_classes = [IsAuthenticated]