import random

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from dragons.models import Dragon


# Create your views here.

class DisplayDragonView(ListView):
    model = Dragon
    template_name = 'dragons/display-page.html'
    context_object_name = 'dragons'
    paginate_by = 3


class RandomDragonView(View):
    def get(self, request):
        dragons= list(Dragon.objects.all())

        if not dragons:
            context = {'dragons':None}
            return render(request,'dragons/display-random-page.html',context)

        random_dragon = random.choice(dragons)
        context = {'dragon':random_dragon}
        return render(request,'dragons/display-random-page.html',context)

# def random_dragon(request: HttpRequest) -> HttpResponse:
#     dragons = Dragon.objects.all()
#     dragon_for_you = random.choice(dragons)
#     context = {
#         'dragon': dragon_for_you,
#     }
#     return render(request, 'dragons/display-random-page.html', context)

# def raise_an_egg(request: HttpRequest) -> HttpResponse:
#     #it needs 10 books readed, 3 magic potions created to create a dragon
#     #it will return how many of each it need more for the dragon to be born
#     return render(request,'dragons/raise-an-egg.html',context)
#
# def create_dragon(request: HttpRequest) -> HttpResponse:
#     #only after raise an egg is succesful, it can have name,powers etc and for cooler to thing of a way to have a
# # random generated picture of a dragon
#     return render(request,'dragons/create-dragon.html',context)