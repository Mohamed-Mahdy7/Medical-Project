from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserCreateSerializer, UserSerializer

# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}