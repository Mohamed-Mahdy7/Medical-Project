 

from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'specialties', views.SpecialtyViewSet, basename='specialty')
router.register(r'', views.DoctorViewSet, basename='doctor')
urlpatterns = router.urls
