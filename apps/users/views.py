from datetime import datetime, timezone
from django.utils.timezone import get_current_timezone
from django.contrib.auth import authenticate, get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import RegisterUserSerializer, UserListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('-id')
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

def token_to_response(response, user):
    refresh_token = RefreshToken.for_user(user)
    refresh_token_str = str(refresh_token)
    refresh_token_exp = datetime.fromtimestamp(
        refresh_token['exp'], tz=get_current_timezone()
    )

    access_token = refresh_token.access_token
    access_token_str = str(access_token)
    access_token_exp = datetime.fromtimestamp(
        access_token['exp'], tz=get_current_timezone()
    )

    response.set_cookie(
        'refresh_token',
        refresh_token_str,
        expires=refresh_token_exp,
        httponly=True
    )
    response.set_cookie(
        'access_token',
        access_token_str,
        expires=access_token_exp,
        httponly=True
    )
    response.data = {
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'refresh_token': refresh_token_str,
        'access_token': access_token_str
    }
    return response


class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    # serializer_class = RegisterSerializer
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return token_to_response(Response(status=status.HTTP_201_CREATED), user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import logging
logger = logging.getLogger(__name__)

class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserListSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Validated data: {serializer.validated_data}")
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)
        if user:
            logger.info(f"User authenticated: {user.username}")
            return token_to_response(Response(status=status.HTTP_200_OK), user)

        logger.error("Authentication failed.")
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutUserView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')
        return response

