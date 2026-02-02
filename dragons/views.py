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

def raise_an_egg(request: HttpRequest) -> HttpResponse:
    #it needs 10 books readed, 3 magic potions created to create a dragon
    #it will return how many of each it need more for the dragon to be born
    return render(request,'dragons/raise-an-egg.html',context)

def create_dragon(request: HttpRequest) -> HttpResponse:
    #only after raise an egg is succesful, it can have name,powers etc and for cooler to thing of a way to have a
# random generated picture of a dragon
    return render(request,'dragons/create-dragon.html',context)