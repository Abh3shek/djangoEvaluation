from django.urls import path
from .views import RegisterView, protected_view, CustomTokenObtainPairView  # Import your custom view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),  # Use custom view here
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("protected/", protected_view, name="protected"),
]
