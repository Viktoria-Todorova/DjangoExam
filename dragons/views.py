import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from potions.models import Potion
from dragons.models import Dragon


# Create your views here.

class DisplayDragonView(ListView):
    model = Dragon
    template_name = 'dragons/display-page.html'
    context_object_name = 'dragons'
    paginate_by = 3




class RandomDragonView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        
        # Check if the user already has a dragon
        dragon = Dragon.objects.filter(rider=user).first()
        if dragon:
            return render(request, 'dragons/display-random-page.html', {'dragon': dragon, 'newly_matched': False})

        # Logic to check if they have found all potions
        # total_recipes_count = len(set(POTION_RECIPES.values()))
        total_recipes_count=2 #todo to make it more
        user_discovered_count = Potion.objects.filter(magician=user).values('name').distinct().count()
        
        can_match = user_discovered_count >= total_recipes_count
        
        if not can_match:
            context = {
                'can_match': False,
                'total_needed': total_recipes_count,
                'user_has': user_discovered_count
            }
            return render(request, 'dragons/display-random-page.html', context)

        # If they are worthy, find a dragon
        available_dragons = list(Dragon.objects.filter(rider__isnull=True))
        
        if available_dragons:
            dragon = random.choice(available_dragons)
            dragon.rider = user
            dragon.save()
            return render(request, 'dragons/display-random-page.html', {'dragon': dragon, 'newly_matched': True, 'can_match': True})
        else:
            return render(request, 'dragons/display-random-page.html', {'dragon': None, 'can_match': True})



# def raise_an_egg(request: HttpRequest) -> HttpResponse:
#     #it needs 10 books readed, 3 magic potions created to create a dragon
#     #it will return how many of each it need more for the dragon to be born
#     return render(request,'dragons/raise-an-egg.html',context)
#
# def create_dragon(request: HttpRequest) -> HttpResponse:
#     #only after raise an egg is succesful, it can have name,powers etc and for cooler to thing of a way to have a
# # random generated picture of a dragon
#     return render(request,'dragons/create-dragon.html',context)