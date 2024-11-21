from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from tutorial.quickstart.views import UserViewSet

from apps.users.views import RegisterView, LoginView, LogoutUserView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutUserView.as_view(), name='user-logout'),
    path('', include(router.urls)),
]
