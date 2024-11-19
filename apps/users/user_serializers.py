# import re
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
# from apps.users.models import CustomUser
#
#

#
#
# class RegisterUserSerializer(serializers.ModelSerializer):
#     re_password = serializers.CharField(
#         max_length=128,
#         write_only=True,
#     )
#
#     class Meta:
#         model = CustomUser
#         fields = (
#             'username',
#             'email',
#             'password',
#             're_password',
#             'role',
#         )
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def validate(self, data):
#         username = data.get('username')
#         if not re.match('^[a-zA-Z0-9_]*$', username):
#             raise serializers.ValidationError(
#                 "The username must be alphanumeric characters or have only _ symbol"
#             )
#
#         password = data.get("password")
#         re_password = data.get("re_password")
#
#         if password != re_password:
#             raise serializers.ValidationError({"password": "Passwords don't match"})
#
#         try:
#             validate_password(password)
#         except ValidationError as err:
#             raise serializers.ValidationError({"password": err.messages})
#
#         return data
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         validated_data.pop('re_password')
#         user = CustomUser(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from apps.users.models import CustomUser

User  = get_user_model()

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'role',
        )


# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password', 'role']
#         extra_kwargs = {'email': {'required': True, 'allow_blank': False,
#                                   'validators': [UniqueValidator(queryset=CustomUser.objects.all())]},
#                         'password': {'write_only': True, 'style': {'input_type': 'password'}}}
#
#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#             email=validated_data['email'],
#             # username=validated_data['email'],
#             role=validated_data['role'],
#         )
#         return user
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     email = serializers.EmailField(required=True)
#
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#             'password',
#         )
#
#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Это имя пользователя уже занято.")
#         return value
#
#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("Этот адрес электронной почты уже используется.")
#         return value
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             # email=validated_data['email'],
#             password=validated_data['password'],
#         )
#         return user
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'role']
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [UniqueValidator(queryset=CustomUser.objects.all())]
            },
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Удаляем confirm_password перед созданием пользователя
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Необходимо указать email и пароль")
        return data

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role']
        extra_kwargs = {'email': {'required': True, 'allow_blank': False},
                        'password': {'write_only': True, 'style': {'input_type': 'password'}}}

