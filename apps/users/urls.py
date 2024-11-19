from django.urls import path
from apps.users.user_views import RegisterView, LogoutUserView, LoginView

urlpatterns = [
    #path('users/list/', UserListGenericView.as_view(), name='user-list'),
    #path('users/register/', RegisterUserGenericView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutUserView.as_view(), name='user-logout'),
    path('register/', RegisterView.as_view(), name='user-register'),
]




