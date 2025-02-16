from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AndroidAppViewSet

router = DefaultRouter()
router.register(r'apps', AndroidAppViewSet, basename='androidapp')

urlpatterns = [
    path('', include(router.urls)),
]
