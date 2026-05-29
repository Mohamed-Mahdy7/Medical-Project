
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, \
    UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name", 
            "password", "confirm_password", "role"
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)

        return user
    
class UserSerializer(BaseUserSerializer):
    is_approved = serializers.BooleanField(read_only=True)
    is_blocked = serializers.BooleanField(read_only=True)
    
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id", "username", "email", "first_name", "last_name", 
            "role", "is_approved", "is_blocked"
        ]
