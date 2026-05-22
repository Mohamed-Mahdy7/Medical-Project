from django.urls import path
from .views import PatientView

urlpatterns = [
    path('patients/me/', PatientView.as_view(), name='patient-profile')
]