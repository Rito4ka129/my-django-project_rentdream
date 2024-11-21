from datetime import datetime, timezone
from django.utils.timezone import get_current_timezone
from django.contrib.auth import authenticate, get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from apps.search.serializers import LogoutSerializer
from apps.users.serializers import RegisterUserSerializer, UserListSerializer, LoginSerializer


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
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            access_token, refresh_token = serializer.get_tokens(serializer.validated_data['user'])

            response = Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )

            return response


class LogoutUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    def post(self, request):
        response = Response(status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
