from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # Note the trailing slash
    path('profile/', UserProfileView.as_view(), name='profile'),
]