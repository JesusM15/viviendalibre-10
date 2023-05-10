from django.shortcuts import render


def central(request):
    return render(request, 'enlaces/central.html')

def seguro_hogar(request):
    return render(request, 'enlaces/seguro_hogar.html')

def quienes_somos(request):
    return render(request, 'enlaces/quienes_somos.html')

def recomendaciones_vendedor(request):
    return render(request, 'enlaces/recomendaciones_vendedor.html')

def ofrecemos_vendedor(request):
    return render(request, 'enlaces/ofrecemos_al_vendedor.html')