from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register('user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name="Login"),
    path('logout/', views.LogoutView.as_view(), name="Logout"),
    path('token-refresh/', TokenRefreshView.as_view(), name="Refresh"),
    ]