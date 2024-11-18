# import re
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
# from apps.users.models import CustomUser
#
#
# class UserListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = (
#             'username',
#             'email',
#             'role',
#         )
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

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            #email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
