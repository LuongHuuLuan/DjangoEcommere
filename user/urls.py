from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api/users/login', views.LoginView.as_view()),
    path('api/users/refresh', views.RefreshTokenView.as_view()),
    path('api/users/register', views.RegisterView.as_view()),
    path('api/users/auth', views.AuthView.as_view()),
    path('api/users/logout', views.LogoutView.as_view()),
]