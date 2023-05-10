from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views import View

class PrincipalView(TemplateView):
    template_name = 'herramientas/enlaces.html'
    
class SimuladorHipoteca(View):
    
    def get(self, request):
        years = ['2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
        context = {
            'years': years,
        }
        return render(request, 'herramientas/paginas/simuladorhipoteca.html', context)