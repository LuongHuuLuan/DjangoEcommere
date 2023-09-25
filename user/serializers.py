from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validate_data):
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password', ''),
        }


class UserResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=255)
    code = serializers.IntegerField()
    data = UserSerializer()
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class TokenResponseSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)
    access_token = serializers.CharField(max_length=255)
    access_expires = serializers.IntegerField()
    refresh_expires = serializers.IntegerField()

class LoginResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=255)
    code = serializers.IntegerField()
    data = TokenResponseSerializer()

class ResponeFailSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255)

class RefreshTokenRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)