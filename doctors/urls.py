from django.urls import path

from .views import (
    SpecialtyListView,
    DoctorListView,
    DoctorDetailView,
    DoctorMeView
)


urlpatterns = [

    path(
        'specialties/',
        SpecialtyListView.as_view(),
        name='specialty-list'
    ),

    path(
        'doctors/',
        DoctorListView.as_view(),
        name='doctor-list'
    ),

    path(
        'doctors/me/',
        DoctorMeView.as_view(),
        name='doctor-me'
    ),

    path(
        'doctors/<int:pk>/',
        DoctorDetailView.as_view(),
        name='doctor-detail'
    ),
]