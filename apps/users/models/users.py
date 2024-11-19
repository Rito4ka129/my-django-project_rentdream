from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('tenant', 'Арендатор'),
        ('landlord', 'Арендодатель'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

# class CustomUser(models.Model):
#     ROLE_CHOICES = (
#         ('tenant', 'Арендатор'),
#         ('landlord', 'Арендодатель'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="CustomUser")
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
#     email = models.EmailField(unique=True)
#     USERNAME_FIELD = "email"
#     EQUIRED_FIELDS = ["username"]
#
#     def __str__(self):
#         return self.user.username
