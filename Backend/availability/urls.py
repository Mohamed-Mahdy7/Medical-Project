from .views import AvailabilityViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()
router.register('availability', AvailabilityViewSet, basename='availability')

urlpatterns = [
    path('', include(router.urls)),
]