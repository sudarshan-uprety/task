from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from utils.exceptions import ConflictException

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )
    full_name = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'confirm_password']

    def validate_email(self, value):
        """
        Validate email after other validations are complete
        """
        if User.objects.filter(email=value).exists():
            raise ConflictException({
                "email": ["Email already registered."]
            })
        return value

    def validate(self, attrs):
        """
        Validate password match 
        """
        if attrs['password'] != attrs.pop('confirm_password'):
            raise ValidationError({
                "confirm_password": "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', '')
        )
        return user


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate_refresh(self, value):
        if not value:
            raise serializers.ValidationError("Refresh token is required.")
        return value

    def validate(self, attrs):
        refresh_token = attrs['refresh']
        token = RefreshToken(refresh_token)

        # Generate new access token
        attrs['access'] = str(token.access_token)
        attrs['refresh'] = str(token)

        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']
