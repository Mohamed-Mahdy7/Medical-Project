
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('user/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('availability/', include('availability.urls')),
    path("appointments/", include("appointments.urls")),
]
