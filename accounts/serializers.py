from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, \
    UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id", "username", "email", "first_name", "last_name", 
            "password", "role", "is_approved", "is_blocked"
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id", "username", "email", "first_name", "last_name", 
            "role", "is_approved", "is_blocked"
        ]
