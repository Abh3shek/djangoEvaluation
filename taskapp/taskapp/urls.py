"""
URL configuration for taskapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import ui_views
from core.views import CustomTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),  # This routes all /api/ requests to the core app
    path("api/", include("apps.urls")),  # Our new apps endpoints
    path("api/", include("tasks.urls")),  # user task endpoints

    # UI endpoints
    path("register-ui/", ui_views.ui_register, name="ui_register"),
    path("login-ui/", ui_views.ui_login, name="ui_login"),
    path("dashboard/", ui_views.dashboard, name="dashboard"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # You can also add a logout view:
    # path("logout-ui/", ui_views.ui_logout, name="ui_logout"),
]
