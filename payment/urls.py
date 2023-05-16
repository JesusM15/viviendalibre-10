from django.urls import path
from . import views

urlpatterns = [
    path('publica-premium/', views.PricingView.as_view(), name='pricing'),
    # path('crear-producto/', views.pago_premium_crear_producto, name='producto_paypal'),
    # path('pago_premium_plan/<str:id_product>/', views.pago_premium_plan, name='pago_premium_plan'),
    path('generar-subscripcion/<str:plan_id>/', views.generar_subscripcion, name='generar_subscripcion'),
    path('paypal/subscriptions/webhook/', views.webhook, name='webhook_paypal'),    
    path('subscripcion/exitosa/', views.pago_exitoso, name='pago_exitoso'),
    path('subscripcion/fallida/', views.pago_fallido, name='pago_fallido'),
]