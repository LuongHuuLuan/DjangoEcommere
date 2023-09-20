import jwt as jwt
from django.shortcuts import render, get_object_or_404
from .models import User
from .serializers import UserSerializer

# from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "created", "data": serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # email = request.data['email']
        # password = request.data['password']
        #
        # user = User.objects.filter(email=email).first()
        #
        # if user is None:
        #     raise AuthenticationFailed('User not found!')
        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect password!')
        #
        # payload = {
        #     'id': user.id,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     'iat': datetime.datetime.utcnow()
        # }
        #
        # token = jwt.encode(payload, 'secret', algorithm='HS256')
        #
        # response = Response()
        #
        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {"status": "success", "token": token}
        # response.status_code = status.HTTP_200_OK
        # return response

        user = get_object_or_404(User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        # serializer = UserSerializer(instance=user)
        return Response({"status": "success", "token": token.key})

class AuthView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # token = request.COOKIES.get('jwt')
        #
        # if not token:
        #     raise AuthenticationFailed('Unauthenticaticated!')
        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unauthenticaticated!')


        # user = User.objects.get(id=payload['id'])
        user = Token.objects.get(key=request.auth.key).user
        serializer = UserSerializer(user)

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):

        # token = request.COOKIES.get('jwt')
        # if not token:
        #     return Response({"status": "failed"}, status=status.HTTP_200_OK)

        response = Response()
        response.delete_cookie('jwt')
        response.data = {"status": "success"}
        response.status_code = status.HTTP_200_OK

        return response