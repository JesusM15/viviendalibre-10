from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from .models import *
from inmuebles.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
import xmltodict
from datetime import timedelta, datetime
from django.urls import reverse
import base64
from time import time
from django.views.decorators.http import require_POST
import json
from requests.auth import HTTPBasicAuth
import hashlib
import requests

@csrf_exempt
def webhook(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    
    if data['event_type'] == 'BILLING.SUBSCRIPTION.CANCELLED':
        plan_id = data['resource']['plan_id']
        status = data['resource']['status']
        id = data['resource']['id']
        subscription = Suscripcion.objects.get(id_suscripcion=id)
        subscription.delete()
        
    if data['event_type'] == 'BILLING.SUBSCRIPTION.EXPIRED':
        id_sus = data['resource']['id']
        subscription = Suscripcion.objects.get(id_suscripcion=id)
        subscription.status = 'EXPIRED'
        subscription.save()
        print('Expirada')
        
    if data['event_type'] == 'BILLING.SUBSCRIPTION.ACTIVATED':
        plan_id = data['resource']['plan_id']
        status = data['resource']['status']
        email = data['resource']['subscriber']['email_address']
        
        plan = Plan.objects.get(paypal_plan_id=plan_id)
        user = User.objects.get(email=email)
        subscription = Suscripcion.objects.get(plan=plan, user=user)
        subscription.status = status
        subscription.save()
        
    if data['event_type'] == 'BILLING.SUBSCRIPTION.CREATED':
        email = data['resource']['subscriber']['email_address']
        plan_id = data['resource']['plan_id']
        sus = data['resource']['id']
        user = User.objects.get(email=email)
        plan = Plan.objects.get(paypal_plan_id=plan_id)
        try:
            subscription = Suscripcion.objects.create(plan=plan, user=user, status='ACTIVE', id_suscripcion=sus)
        except:
            pass
        print('Suscripcion creada')
            
    if data['event_type'] == 'PAYMENT.SALE.COMPLETED':
        id_sus = data['resource']['billing_agreement_id']
        subscription = Suscripcion.objects.get(id_suscripcion=id_sus)
        subscription.status = 'ACTIVE'
        subscription.save()
        print('Pago realizado')
                
    return HttpResponse()

class PricingView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        premium = Plan.objects.get(name='Plan premium')
        context = {"premium": premium,}
        
        return render(request, 'payment/precios.html', context)
    
@login_required
def pago_premium_crear_producto(request):    
    data = {
            "client_id":settings.CLIENT_ID,
            "client_secret":settings.SECRET_KEY_PAYPAL,
            "grant_type":"client_credentials"
    }
    headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic {0}".format(base64.b64encode((settings.CLIENT_ID + ":" + settings.SECRET_KEY_PAYPAL).encode()).decode())
            }
    url = settings.HEADERS_URL
    
    token = requests.post(url, data, headers=headers)
    token = token.json()['access_token']
    
    headers_2 = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    
    data_2 = {
                "name": "Plan-premium",
                "description": "Subscripcion a premium mensual",
                "type": "SERVICE",
                "category":  "SOFTWARE",
            }
        
    response = requests.post(f'{settings.PAYPAL_API}/v1/catalogs/products', json = data_2, headers=headers_2, timeout=60)
    if response:
        plan = Plan.objects.get(name="Plan premium")
        paypal_id = "".join(response.json()['id'])
        plan.paypal_id = paypal_id
        plan.save()
        
        return redirect(reverse('pago_premium_plan', args=[paypal_id]))
    return HttpResponse('Todo mal')

@login_required
def pago_premium_plan(request, id_product):
    body = Plan.objects.get(paypal_id=id_product)
    data = {
            "client_id":settings.CLIENT_ID,
            "client_secret":settings.SECRET_KEY_PAYPAL,
            "grant_type":"client_credentials"
    }
    headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic {0}".format(base64.b64encode((settings.CLIENT_ID + ":" + settings.SECRET_KEY_PAYPAL).encode()).decode())
            }
    url = settings.HEADERS_URL
    
    token = requests.post(url, data, headers=headers)
    token = token.json()['access_token']
    
    plan = {
        'name': 'Plan 6 meses', 
        'product_id': body.paypal_id,
        "status": "ACTIVE",
        "description": body.description,
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": 6
                },
                "tenure_type": "REGULAR",
                "sequence": 1,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": 10,
                        "currency_code": "USD",
                    },
                }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {
                "value": 0,
                "currency_code": "USD"
            }
        },
        "taxes": {
            "percentage": "10",
            "inclusive": False,
        }
    }
    headers_2 = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    
    response = requests.post(f'{settings.PAYPAL_API}/v1/billing/plans', json = plan, headers=headers_2, timeout=120)
    if response:
        id = "".join(response.json()['id'])
        body.paypal_plan_id = id
        body.save()
        return HttpResponse("Todo OK")
    return HttpResponse("Todo mal")
    
@login_required
def generar_subscripcion(request, plan_id):
    plan = get_object_or_404(Plan, paypal_plan_id=plan_id)
    user = get_object_or_404(User, pk=request.user.pk, email=request.user.email)
    
    data = {
        "client_id":settings.CLIENT_ID,
        "client_secret":settings.SECRET_KEY_PAYPAL,
        "grant_type":"client_credentials"
    }
    headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic {0}".format(base64.b64encode((settings.CLIENT_ID + ":" + settings.SECRET_KEY_PAYPAL).encode()).decode())
            }
    url = settings.HEADERS_URL
    
    token = requests.post(url, data, headers=headers)
    token = token.json()['access_token']
    
    headers_2 = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    d = datetime.utcnow() + timedelta(minutes=4)
    subscription = {
        "plan_id": plan.paypal_plan_id,
        "start_time":  str(d.isoformat("T") + "Z") ,
        "quantity": 1,
        "subscriber": {
            "name": {
                "given_name": user.username,
                "surname": user.username
            },
            "email_address": user.email
        }, 
        #paginas donde vamos a redireccionar al cliente si el pago es exitoso o fallido
        "application_context": {
            "return_url": settings.BASE_HOST + 'pago/subscripcion-premium/exitosa/',
            "cancel_url": settings.BASE_HOST + 'pago/subscripcion-premium/fallida/'       
        }   
    }
    
    response = requests.post(f'{settings.PAYPAL_API}/v1/billing/subscriptions', json = subscription, headers=headers_2, timeout=120)
    
    r = response.json()['links'][0]['href']
    
    return render(request, 'payment/pagar.html', {'link': r})

def pago_fallido(request):
    return render(request, 'payment/fail.html')

def pago_exitoso(request):
    subscription_id = request.GET['subscription_id']
    ba_token = request.GET['ba_token']
    token = request.GET['token']
    
    return render(request, 'payment/success.html')