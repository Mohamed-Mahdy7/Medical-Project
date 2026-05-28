from xmlrpc.client import ResponseError

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserCreateSerializer, UserSerializer

# Create your views here.

class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    
    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        
        return UserSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        response =  super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access = response.data.get('access')
            refresh = response.data.get('refresh')
            
            response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
            
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=False,
                samesite="Lax"
            )
            
            response.data = {
                "message": "Login Successfully!"
            }
            
        return response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.COOKIES)
        print(request.user)
        print(request.auth)
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                print(f"\n Error While Logging out!: {str(e)}\n" )
                return Response({
                    "Error While Logging out" : str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        response = Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )
        
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        return response
