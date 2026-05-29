from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from appointments.permissions import IsPatient
from .models import PatientProfile
from .serializers import PatientProfileSerializer


class PatientProfileViewSet(ModelViewSet):

    permission_classes = [IsPatient]
    serializer_class = PatientProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender']

    http_method_names = ['get', 'put', 'patch', 'head', 'options']

    def get_object(self):
        profile, _ = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_queryset(self):
        return PatientProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request):
        profile = self.get_object()

        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response({
                "status": "success",
                "message": "Patient profile retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
            "status": "success",
            "message": "Patient profile updated successfully.",
            "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)