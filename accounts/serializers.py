from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id", "username", "email", "first_name", "last_name", 
            "password", "role", "is_approved", "is_blocked"
        ]