from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage, name='home'),
    path('aviso-maxima-cantidad-de-inmuebles/', max_post, name='max_post'),
    path('filtrado/', HomePageFilter, name='home_filter'),
    path('publicar-inmueble/', create_post, name='crear_publicacion'),
    path('detalles/<slug:inmueble_slug>/', inmueble_detail, name='detalles'),
    path('mis-publicaciones/<str:username>/<str:user_email>/', mis_inmuebles, name='mis_inmuebles'),
    path('eliminar-mi-inmueble/<str:user_email>/<int:inmueble_id>/<slug:inmueble_slug>/', confirmar_delete, name='confirmar_delete'),
    path('eliminando-inmueble/<str:user_email>/<int:inmueble_id>/<slug:inmueble_slug>/', delete_confirmado, name='delete_confirmado'),
    path('editar-mi-inmueble/<str:user_email>/<int:inmueble_id>/<slug:inmueble_slug>/', edit_inmueble, name='edit_inmueble'),    
    path('enviar-email/<int:inmueble_id>/', sent_email_to_seller, name='sent_email_to_seller'),
]