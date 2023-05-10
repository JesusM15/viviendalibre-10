from django.urls import path
from . import views

urlpatterns = [
    path('central/', views.central, name='enlaces_de_interes'),
    path('seguro-de-hogar/', views.seguro_hogar, name='seguro_hogar'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('recomendaciones-al-vendedor/', views.recomendaciones_vendedor, name='recomendaciones_vendedor'),
    path('que-ofrecemos-al-vendedor/', views.ofrecemos_vendedor, name='ofrecemos_vendedor'),
    
]