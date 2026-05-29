 

from django.urls import path
from .views import SpecialtyViewSet, DoctorViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'specialties', SpecialtyViewSet, basename='specialty')
router.register(r'doctors', DoctorViewSet, basename='doctor')   
urlpatterns = router.urls
