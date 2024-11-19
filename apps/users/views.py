# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.serializers import UserRegistrationSerializer, TokenRefreshSerializer
from utils.response import CustomResponse


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }

        return CustomResponse.success(
            data=user_data,
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED
        )


class UserLogin(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return CustomResponse.success(
            message="Login successful",
            data=serializer.validated_data,
            status_code=status.HTTP_200_OK
        )


class UserRefreshTokenView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return CustomResponse.success(
            message="Token refreshed successfully",
            data=serializer.validated_data,
            status_code=status.HTTP_200_OK
        )

