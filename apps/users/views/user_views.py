from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from tutorial.quickstart.serializers import UserSerializer
from apps.users.models import User
from apps.users.serializers.user_serializers import *
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class UserListGenericView(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        project_name = self.request.query_params.get('project_name')

        if project_name:
            return User.objects.filter(project__name=project_name)

        return User.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        users = self.get_queryset()

        if not users.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = self.get_serializer(users, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class RegisterUserGenericView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class LoginUserView(APIView):
#     permission_classes = [permissions.AllowAny]
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         user = User.objects.filter(email=email).first()
#         username = user.username if user is not None else ''
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#
#         if user:
#             response = Response(status=status.HTTP_200_OK)
#             refresh_token = RefreshToken.for_user(user)
#             refresh_token_str = str(refresh_token)
#             refresh_token_exp = refresh_token['exp']
#             refresh_token_exp = timezone.datetime.fromtimestamp(
#                 refresh_token_exp,
#                 tz=timezone.get_current_timezone()
#             )
#             access_token = refresh_token.access_token
#             access_token_str = str(access_token)
#             access_token_exp = access_token['exp']
#             access_token_exp = timezone.datetime.fromtimestamp(
#                 access_token_exp,
#                 tz=timezone.get_current_timezone()
#             )
#             response.set_cookie(
#                 'refresh_token',
#                 refresh_token_str,
#                 expires=refresh_token_exp,
#                 httponly=True
#             )
#             response.set_cookie(
#                 'access_token',
#                 access_token_str,
#                 expires=access_token_exp,
#                 httponly=True
#             )
#             response.data = {
#                 'username': user.username,
#                 'email': user.email,
#                 'refresh_token': refresh_token_str,
#                 'access_token': access_token_str
#             }
#         else:
#             return Response({'details': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class LoginUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'details': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'details': 'User  not found'}, status=status.HTTP_404_NOT_FOUND)

        username = user.username
        user = authenticate(request, username=username, password=password)

        if user:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            response = Response({
                'username': user.username,
                'email': user.email,
                'refresh_token': str(refresh_token),
                'access_token': str(access_token)
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                'refresh_token',
                str(refresh_token),
                expires=timezone.datetime.fromtimestamp(refresh_token['exp'], tz=timezone.get_current_timezone()),
                httponly=True
            )
            response.set_cookie(
                'access_token',
                str(access_token),
                expires=timezone.datetime.fromtimestamp(access_token['exp'], tz=timezone.get_current_timezone()),
                httponly=True
            )
            return response
        else:
            return Response({'details': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')
        return response





