from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

from allauth.account.signals import email_confirmed

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class Image(models.Model):
    image = models.ImageField(blank=True, null=True)
    
    def __unicode__(self):
        return str(self.image)

class Ubicacion(models.Model):
    departamento = models.CharField(max_length=300)
    provincia = models.CharField(max_length=300)
    codigo_p = models.IntegerField(null=True, blank=True)
    ciudad = models.CharField(max_length=300)
    
    def __str__(self):return f'{self.departamento}, {self.provincia}, {self.ciudad}'
    
class Pricing(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    stripe_price_id = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions')
    created = models.DateTimeField(auto_now_add=True)
    stripe_subscription_id = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['-created',] 
        
    def __str__(self):
        return self.user.email
    
    @property
    def is_active(self):
        return self.status == "active" or self.status == "trialing"
    
class Plan(models.Model):
    name = models.CharField(max_length=400) 
    slug = models.SlugField(unique=True)
    paypal_id = models.CharField(max_length=500, blank=True)
    paypal_plan_id = models.CharField(max_length=500, blank=True)
    currency = models.CharField(max_length=60, default="COP")
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    
    def __str__(self): return self.name  
    
class Suscripcion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="suscripciones")
    id_suscripcion = models.CharField(max_length=560, blank=True)
    ba_token = models.CharField(max_length=560, blank=True)
    token = models.CharField(max_length=560, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.plan.name}{self.created}')
        super().save(*args, **kwargs)
    
    def __str__(self): return self.user.email
    
#modelo de los inmuebles
class Inmueble(models.Model):
    
    #choices
    class Estado(models.TextChoices):
        NUEVO = 'Obra nueva', 'Obra nueva'
        USADO = 'Usado', 'Usado'        
    
    PREGUNTAS_CERRADAS = [(True, 'Si'), (False, 'No')]
 
    TIPO_INMUEBLE = [
        ('Casa', 'Casa'),('Apartamento', 'Apartamento'),('Local', 'Local'),('Oficina', 'Oficina'),('Bodega', 'Bodega'),('Vivienda vacacional', 'Vivienda vacacional'),
    ]
    
    TIPO_OPERACION = [('Venta', 'Venta'),('Arriendo', 'Arriendo'),('Permuta', 'Permuta'),]
        
    Tipo_de_inmueble = models.CharField(choices=TIPO_INMUEBLE, max_length=100, default='Casa')
    operacion = models.CharField(choices=TIPO_OPERACION, max_length=100, default='Venta')
    # ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    # codigo_postal = models.PositiveIntegerField()
    ubicacion = models.TextField()
    Lat = models.CharField(max_length=140)
    Lng = models.CharField(max_length=140)
    precio = models.BigIntegerField()
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.NUEVO)
    portada = models.ImageField(upload_to='media/inmuebles/portadas/%Y/%m/%d')
    video = models.FileField(upload_to='media/inmuebles/videos/%Y/%m/%d', null=True, blank=True)
    image = models.ManyToManyField(Image, blank=True, related_name='inmueble')
    
    area = models.PositiveIntegerField()
    habitaciones = models.PositiveIntegerField()
    banos = models.CharField(max_length=6)
    valor_administracion = models.CharField(max_length=200, blank=True, null=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    estrato = models.PositiveIntegerField(blank=True, null=True)
    antiguedad = models.PositiveIntegerField(default=0, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    parqueadero = models.BooleanField(choices=PREGUNTAS_CERRADAS, default=False)
    zonas_verdes = models.BooleanField(choices=PREGUNTAS_CERRADAS, default=False)
    zonas_ninos = models.BooleanField(choices=PREGUNTAS_CERRADAS, default=False)
    zona_comercial = models.BooleanField(choices=PREGUNTAS_CERRADAS, default=False)
    zona_residencial = models.BooleanField(choices=PREGUNTAS_CERRADAS, default=False)
    estudio = models.BooleanField(choices=PREGUNTAS_CERRADAS, default=False)
    published = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, max_length=255, unique_for_date='published')
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    pricing_tiers = models.ManyToManyField(Pricing, blank=True)

    def __str__(self):
        return f'{self.Tipo_de_inmueble} de {self.vendedor.username} en {self.ubicacion}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.Tipo_de_inmueble}{self.pk} en {self.vendedor.id}{self.ubicacion}')
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-creado']
    
    