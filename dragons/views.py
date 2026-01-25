import random

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from dragons.models import Dragon


# Create your views here.

def display_dragons(request: HttpRequest) -> HttpResponse:
    dragons = Dragon.objects.all()
    context = {
        'dragons': dragons,
    }
    return render(request, 'dragons/display-page.html', context)


def random_dragon(request: HttpRequest) -> HttpResponse:
    dragons = Dragon.objects.all()
    dragon_for_you = random.choice(dragons)
    context = {
        'dragon': dragon_for_you,
    }
    return render(request, 'dragons/display-random-page.html', context)