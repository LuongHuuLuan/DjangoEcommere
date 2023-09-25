from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, UserLoginSerializer, \
    LoginResponseSerializer, UserResponseSerializer, RefreshTokenRequestSerializer, \
    ResponeFailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiExample


# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={201: UserResponseSerializer, 400: ResponeFailSerializer},
        examples=[
            OpenApiExample(
                'Example',
                value={
                    "status": "success",
                    "code": 200,
                    "data": {
                        "name": "John Doe",
                        "password": "examplepassword",
                        "email": "johndoe@example.com"
                    }
                },
                request_only=True,
            ),
            OpenApiExample(
                "Account created",
                status_codes=[201],
                value={
                    "status": "created",
                    "code": 201,
                    "data": {
                        "id": 1,
                        "name": "John Doe",
                        "email": "johndoe@example.com"
                    }
                },
                response_only=True,
            ),
            OpenApiExample(
                "Email exists",
                status_codes=[400],
                value={
                    "status": "fail",
                    "code": 400,
                    "data": {
                        "message": "User with this email already exists"
                    }
                },
                response_only=True,
            )
        ],
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = serializer.save()
            return Response({"status": "created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User with this email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserLoginSerializer,
        responses={200: LoginResponseSerializer, 401: ResponeFailSerializer},
        examples=[
            OpenApiExample(
                'Example',
                value={
                    "email": "johndoe@example.com",
                    "password": "examplepassword",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example",
                status_codes=[200],
                value={
                    "status": "success",
                    "code": 200,
                    "data": {
                        "refresh_token": "eb37dceaa22cd894fa1952237571449xxxxxxxxx",
                        "access_token": "eb37dceaa22cd894fa1952237571449xxxxxxxxx",
                        "access_expires": 3600,
                        "refresh_expires": 86400
                    }
                },
                response_only=True,
            ),
            OpenApiExample(
                "User not found",
                status_codes=[401],
                value={
                    "status": "fail",
                    "code": 401,
                    "data": {
                        "message": "User not found"
                    }
                },
                response_only=True,
            ),
            OpenApiExample(
                "Incorrect password",
                status_codes=[401],
                value={
                    "status": "fail",
                    "code": 401,
                    "data": {
                        "message": "Incorrect password"
                    }
                },
                response_only=True,
            )
        ],
    )
    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(request,
                                username=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                return Response({
                    "status": "success",
                    "code": 200,
                    "data": {
                        'refresh_token': str(refresh),
                        'access_token': str(refresh.access_token),
                        'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                        'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                    }
                })
            else:
                return Response({
                    "status": "fail",
                    'code': 400,
                    "data": {'message': 'Email or password is incorrect!'}
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "fail",
                'code': 400,
                "data": {
                    'message': serializer.errors,

                }
            }, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RefreshTokenRequestSerializer,
        responses={200: LoginResponseSerializer, 400: ResponeFailSerializer},
        examples=[
            OpenApiExample(
                'Example',
                value={
                    "token": "eb37dceaa22cd894fa1952237571449xxxxxxxxx",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example",
                status_codes=[200],
                value={
                    "status": "success",
                    "code": 200,
                    "data": {
                        "refresh_token": "eb37dceaa22cd894fa1952237571449xxxxxxxxx",
                        "access_token": "eb37dceaa22cd894fa1952237571449xxxxxxxxx",
                        "access_expires": 3600,
                        "refresh_expires": 86400
                    }
                },
                response_only=True,
            ),
            OpenApiExample(
                "Example",
                status_codes=[400],
                value={
                    "status": "fail",
                    "code": 400,
                    "data": {
                        "message": "Not found token value in body"
                    }
                },
                response_only=True,
            )
        ],
    )
    def post(self, request):
        try:
            token = RefreshToken(request.data["token"])
            return Response({
                "status": "success",
                "code": 200,
                "data": {
                    'refresh_token': str(token),
                    'access_token': str(token.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                }
            })
        except Exception as e:
            return Response({
                "status": "fail",
                'code': 400,
                "data": {
                    'message': "Not found token value in body",
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class AuthView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserResponseSerializer, 401: ResponeFailSerializer},
        examples=[
            OpenApiExample(
                "Example",
                status_codes=[200],
                value={
                    "status": "success",
                    "code": 200,
                    "data": {
                        "name": "John Doe",
                        "password": "examplepassword",
                        "email": "johndoe@example.com"
                    }
                },
                response_only=True,
            ),
            OpenApiExample(
                "No token header",
                status_codes=[401],
                value={
                    "status": "fail",
                    "code": 401,
                    "data": {
                        "message": "Authentication credentials were not provided"
                    }
                },
                response_only=True,
            ),
            OpenApiExample(
                "Invalid token",
                status_codes=[401],
                value={
                    "status": "fail",
                    "code": 401,
                    "data": {
                        "message": "Invalid token"
                    }
                },
                response_only=True,
            ),
        ],
    )
    def get(self, request):
        JWT_authenticator = JWTAuthentication()
        authenticate = JWT_authenticator.authenticate(request)
        user, token = authenticate
        userData = User.objects.get(email=user)
        serializer = UserSerializer(userData)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    serializer_class = None
    def post(self, request):
        response = Response()
        response.delete_cookie('Token')
        response.data = {"status": "success"}
        response.status_code = status.HTTP_200_OK

        return response
