from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer

# Create your views here.
class PatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user):
        profile, created = Patient.objects.get_or_create(user=user)
        return profile
    
    def get(self, request):
        profile = self.get_object(request.user)
        serializer = PatientSerializer(profile)
        return Response({
            "status": "success",
            "message": "Patient profile retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request):
        profile = self.get_object(request.user)
        serializer = PatientSerializer(profile, data=request.data, partial=True)
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
