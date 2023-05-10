from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('registrarse/', register, name='register'),
    
    path('iniciar-sesion/', auth_views.LoginView.as_view(), name='login'),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(), name='logout'),
    
]