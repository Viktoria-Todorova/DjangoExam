from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from catalog.models import Catalog


# Create your views here.
def home(request: HttpRequest)->HttpResponse:
    context = {
        'catalog': Catalog.objects.all(),
    }

    return render(request, 'home.html', context)