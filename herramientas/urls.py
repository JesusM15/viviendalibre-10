from django.urls import path
from . import views

urlpatterns = [
    path('enlaces-de-interes/', views.PrincipalView.as_view(), name='enlaces'),
    path('simulador-de-hipoteca/', views.SimuladorHipoteca.as_view(), name='simulador_hipoteca'),
]