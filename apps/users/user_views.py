# from datetime import datetime
# from django.utils import timezone
# from django.contrib.auth import authenticate
# from rest_framework.permissions import AllowAny
# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from rest_framework.generics import ListAPIView, CreateAPIView
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from apps.users.models.users import CustomUser
# from apps.users.user_serializers import UserListSerializer, RegisterUserSerializer
from datetime import datetime, timezone

from django.contrib.auth import authenticate

from rest_framework.request import Request

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .user_serializers  import RegisterSerializer


# class UserListGenericView(ListAPIView):
#     serializer_class = UserListSerializer
#
#     def get_queryset(self):
#         project_name = self.request.query_params.get('project_name')
#         if project_name:
#             return CustomUser.objects.filter(project__name=project_name)
#         return CustomUser.objects.all()
#
#     def list(self, request: Request, *args, **kwargs) -> Response:
#         users = self.get_queryset()
#         if not users.exists():
#             return Response(data=[], status=status.HTTP_204_NO_CONTENT)
#
#         serializer = self.get_serializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
# class RegisterUserGenericView(CreateAPIView):
#     serializer_class = RegisterUserSerializer
#     permission_classes = [AllowAny]
#
#     def create(self, request: Request, *args, **kwargs) -> Response:
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         # Проверка на существование пользователя с таким же email
#         if CustomUser.objects.filter(email=request.data.get('email')).exists():
#             return Response({'details': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         serializer.save()
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
class LoginUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'details': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Аутентификация пользователя по email
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            return Response({'details': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request, username=user.username, password=password)
        if user is None:
            return Response({'details': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

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
            expires=datetime.fromtimestamp(refresh_token['exp'], tz=timezone.utc),
            httponly=True,
            samesite='Lax'  # Вы можете изменить это значение в зависимости от ваших требований
        )
        response.set_cookie(
            'access_token',
            str(access_token),
            expires=datetime.fromtimestamp(access_token['exp'], tz=timezone.utc),
            httponly=True,
            samesite='Lax'  # Вы можете изменить это значение в зависимости от ваших требований
        )
        return response

class LogoutUserView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')
        return response



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
