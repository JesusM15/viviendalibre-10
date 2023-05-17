from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
User = get_user_model()
from .forms import *
from .models import *
from itertools import chain
from django.db.models import Q
import csv
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives

def HomePage(request):
    
    if request.user:
        if request.user.telefono == '1' or  not request.user.telefono:return redirect(reverse('completar_perfil'))
        
    key = settings.MAPS_API_KEY
            
    inmuebles_1 = Inmueble.objects.filter(vendedor__suscripcion__status="ACTIVE", vendedor__suscripcion__plan__name="Plan premium")
    inmuebles_2 = Inmueble.objects.exclude(vendedor__suscripcion__status="ACTIVE", vendedor__suscripcion__plan__name="Plan premium")
    
    inmuebles_list = list(chain(inmuebles_1, inmuebles_2))
    
    paginator = Paginator(inmuebles_list, 5)
    page_number = request.GET.get('pagina', 1)
    
    try:
        inmuebles = paginator.page(page_number)
    except PageNotAnInteger:
        inmuebles = paginator.page(1)
    except EmptyPage:
        inmuebles = paginator.page(paginator.num_pages)
   
    context = {'inmuebles': inmuebles, 'key': key,}
    return render(request, 'inmuebles/home.html', context)

@login_required
def sent_email_to_seller(request, inmueble_id):
    inmueble = Inmueble.objects.get(pk=inmueble_id)
    inmueble_slug = inmueble.slug
    subject = f'A {request.user.email} le intereso tu inmueble'
    contenido = f'Te recomendamos comunicarte con el\nEn caso de querer hacer lo este es su correo electronico: {request.user.email}\nlink de tu inmueble: {settings.BASE_HOST}detalles/{inmueble_slug}/'
    message = EmailMultiAlternatives(subject,
                                    contenido,
                                    settings.EMAIL_HOST_USER,
                                    [inmueble.vendedor.email,]
                                    )
    message.send()
    
    return redirect(reverse('detalles', args=[inmueble.slug]))

def HomePageFilter(request, search='', operacion='', tipo='', ordenar='-precio', max_range='0', min_range='9223372036854775806'):
    key = settings.MAPS_API_KEY
    search = request.GET.get('search', '')
    operacion = request.GET.get('operacion', '')
    tipo = request.GET.get('tipo', '')
    min_range = request.GET.get('min_range', '0')
    max_range = request.GET.get('max_range', '9223372036854775806')
    
    texto = ''
    texto_ubi = ''
    inmuebles = ''
    if search != '':
        texto_ubi = f'\nbusqueda: {search}'
    if operacion != '' and tipo != '':
        inmuebles = Inmueble.objects.filter(operacion=operacion, Tipo_de_inmueble=tipo, precio__range=[int(min_range), int(max_range)]).filter(ubicacion__icontains=search).order_by(ordenar, '-published')
        texto = f'Mostrando solo: {tipo} y en {operacion}' + texto_ubi
    elif operacion != '' and tipo == '':
        inmuebles = Inmueble.objects.filter(operacion=operacion, precio__range=[int(min_range), int(max_range)]).filter(ubicacion__icontains=search).order_by(ordenar, '-published')
        texto = f'Mostrando solo: {operacion}s' + texto_ubi
    elif tipo != '' and operacion == '':
        inmuebles = Inmueble.objects.filter(Tipo_de_inmueble=tipo, precio__range=[int(min_range), int(max_range)]).filter(ubicacion__icontains=search).order_by(ordenar, '-published')
        texto = f'Mostrando solo: {tipo}' + texto_ubi
    elif tipo == '' and operacion == '':
        inmuebles = Inmueble.objects.filter(ubicacion__icontains=search, precio__range=[int(min_range), int(max_range)]).order_by(ordenar, '-published')
        inmuebles_1 = inmuebles.filter(vendedor__suscripcion__status="ACTIVE", vendedor__suscripcion__plan__name='Plan premium')
        inmuebles_2 = inmuebles.exclude(vendedor__suscripcion__status="ACTIVE", vendedor__suscripcion__plan__name='Plan premium')
        inmuebles = list(chain(inmuebles_1, inmuebles_2))
        texto = f'Busqueda {search}'
        
    inmuebles_list = inmuebles
    paginator = Paginator(inmuebles_list, 5)
    page_number = request.GET.get('pagina', 1)
    
    try:
        inmuebles = paginator.page(page_number)
    except PageNotAnInteger:
        inmuebles = paginator.page(1)
    except EmptyPage:
        inmuebles = paginator.page(paginator.num_pages)

    
    context = {'inmuebles': inmuebles,'texto':texto, 'key': key,}
    return render(request, 'inmuebles/home.html', context)

@login_required
def completar_perfil(request):
    user = request.user
    if request.method == 'POST':
        form = UserCompleteForm(request.POST, instance=user)
        if form.is_valid():
            user_new_info = form.save()
            user_new_info.save()
            return redirect(reverse('home'))
        return render(request, 'accounts/edit_profile.html')
    else:
        form = UserCompleteForm(instance=user)
        return render(request, 'accounts/edit_profile.html', {'form':form,})
    

@login_required
def max_post(request):
    return render(request, 'inmuebles/max_post.html')

@login_required
def create_post(request):
    user = request.user
    inmuebles = Inmueble.objects.filter(vendedor=user)
    if inmuebles.count() > 0:return redirect(reverse('home'))
    key = settings.MAPS_API_KEY

    if request.method == 'POST':
        inmueble_form =InmuebleForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if inmueble_form.is_valid():

            new_inmueble = inmueble_form.save(commit=False)
            new_inmueble.vendedor = request.user
            new_inmueble.ubicacion = request.POST['ubicacion']
            new_inmueble.save()
            
            for i in files:
                img = Image(image=i)
                img.save()
                new_inmueble.image.add(img)
                
            return redirect('home')
    else:
        inmueble_form = InmuebleForm()
    return render(request, 'inmuebles/gestion/crear.html', {'inmueble_form': inmueble_form, 'key':key,})

def inmueble_detail(request, inmueble_slug):
    inmueble = get_object_or_404(Inmueble, slug = inmueble_slug)
    key = settings.MAPS_API_KEY
    context = {'inmueble': inmueble, 'key': key,}
    return render(request, 'inmuebles/detalles.html', context)

@login_required
def mis_inmuebles(request, username, user_email):
    user = get_object_or_404(User, pk=request.user.pk, email=user_email, username=username)
    inmuebles_list = Inmueble.objects.filter(vendedor=user).order_by('-creado')
    paginator = Paginator(inmuebles_list, 5)
    page_number = request.GET.get('pagina', 1)
    
    try:
        inmuebles = paginator.page(page_number)
    except PageNotAnInteger:
        inmuebles = paginator.page(1)
    except EmptyPage:
        inmuebles = paginator.page(paginator.num_pages)

    context = {'inmuebles': inmuebles, }
    
    
    return render(request, 'inmuebles/gestion/mis_inmuebles.html', context)
    
@login_required
def confirmar_delete(request, user_email, inmueble_id, inmueble_slug):
    user = get_object_or_404(User, pk=request.user.pk, email=user_email)
    inmueble = get_object_or_404(Inmueble, pk=inmueble_id, slug=inmueble_slug, vendedor=user)

    context = {'inmueble': inmueble, }
    return render(request, 'inmuebles/gestion/confirmar_delete.html', context)

@login_required
def delete_confirmado(request, user_email, inmueble_id, inmueble_slug):
    user = get_object_or_404(User, pk=request.user.pk, email=user_email)
    inmueble = get_object_or_404(Inmueble, pk=inmueble_id, slug=inmueble_slug, vendedor=user)
    
    inmueble.delete()
    
    return redirect(reverse('mis_inmuebles', args=[user.username, user.email]))

@login_required
def edit_inmueble(request, user_email, inmueble_id, inmueble_slug):
    user = get_object_or_404(User, pk=request.user.pk, email=user_email)
    inmueble = get_object_or_404(Inmueble, pk=inmueble_id, slug=inmueble_slug, vendedor=user)
    key = settings.MAPS_API_KEY
    
    if request.method == 'POST':
        form = InmuebleEditForm(request.POST, request.FILES,  instance=inmueble)
        if form.is_valid():
            inmueble_mod = form.save(commit = False)
            inmueble_mod.ubicacion = request.POST['ubicacion']
            inmueble_mod.save()
                
            return redirect(reverse('mis_inmuebles', args=[user.username, user.email]))
    else:
        form = InmuebleEditForm(instance=inmueble)
        context = {'inmueble': inmueble, 'key': key,}
        return render(request, 'inmuebles/gestion/editar_inmueble.html', context)

def import_archive(request):
    ubicaciones = []
    with open("ubicaciones.csv", "r", encoding="utf8") as csv_file:
        data = list(csv.reader(csv_file, delimiter=","))
        for row in data[1:]:
            ubicaciones.append(
                Ubicacion(
                    departamento=row[0],
                    provincia=row[1],
                    codigo_p=row[2],
                    ciudad=row[3],
                )
            )
    if len(ubicaciones) > 0:
        Ubicacion.objects.bulk_create(ubicaciones)
    
    return HttpResponse("Successfully imported")