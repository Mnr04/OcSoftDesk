from django.urls import path
from .views import user_manager_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/', user_manager_view, name='user-create'),
    path('users/<int:pk>/', user_manager_view, name='user-detail'),
]