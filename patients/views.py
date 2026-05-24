from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from appointments.permissions import IsPatient
from .models import PatientProfile
from .serializers import PatientProfileSerializer


class PatientProfileViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericViewSet):

    permission_classes = [IsPatient]
    serializer_class = PatientProfileSerializer

    def get_object(self):
        profile, _ = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile

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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Patient profile updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)