from django.urls import path

from apps.users.views.user_views import *

urlpatterns = [
    path('users/', UserListGenericView.as_view(), name='user-list'),
    path('users/register/', RegisterUserGenericView.as_view(), name='user-register'),
    path('users/login/', LoginUserView.as_view(), name='user-login'),
    path('users/logout/', LogoutUserView.as_view(), name='user-logout'),
]



# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     # path('user/<int:pk>/', UserView.as_view(), name='user'),
#     path('user/<int:pk>/', UserView.as_view({'get': 'retrieve'}), name='user'),
#
# ]
