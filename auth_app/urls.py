from django.urls import path
from .views import RegisterView
from .views import UserListView
from .views import profile_view, update_profile_view, change_password_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile_view, name='update_profile'),
    path('profile/change_password/', change_password_view, name='change_password'),
]
