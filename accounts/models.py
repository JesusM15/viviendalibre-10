from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    stripe_customer_id = models.CharField(max_length=150)
    creditCardTokenId = models.TextField(blank=True)
    payer_id_paypal = models.TextField(blank=True)