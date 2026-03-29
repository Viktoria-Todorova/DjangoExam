import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from .choices import POTION_RECIPES, FAIL_POTIONS, HERB_DICT, LIQUID_DICT, ITEM_DICT
from .forms import CreatePotionForm
from .models import Potion, SecretPotions


class CreatePotionView(LoginRequiredMixin,FormView):
    template_name = "potions/create-potions.html"
    form_class = CreatePotionForm
    success_url = reverse_lazy('create_potion')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        herb = form.cleaned_data["herb"]
        liquid = form.cleaned_data["liquid"]
        item = form.cleaned_data["item"]
        ingredients = (herb, liquid, item)

        if ingredients in POTION_RECIPES:
            potion_name = POTION_RECIPES[ingredients]
            
            if Potion.objects.filter(name=potion_name, magician=self.request.user).exists():
                result = "already_learned"
            else:
                result = "success"
                Potion.objects.create(
                    name=potion_name,
                    magician=self.request.user,
                    description=f"Brewed with {herb}, {liquid}, and {item}."
                )
        else:
            potion_name = random.choice(FAIL_POTIONS)
            result = "fail"

        context = self.get_context_data(form=form)
        context["result"] = result
        context["potion_name"] = potion_name
        return self.render_to_response(context)


class SecretPotionsView(ListView):
    model = SecretPotions
    template_name = 'potions/potions-details.html'
    context_object_name = "potions"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        potions = context["potions"]

        potions_display = []
        for potion in potions:
            potion.actual_name = {
                "herb": HERB_DICT.get(potion.herb, potion.herb),
                "liquid": LIQUID_DICT.get(potion.liquid, potion.liquid),
                "items": ITEM_DICT.get(potion.items, potion.items),
            }
            potions_display.append(potion)

        context["potions"] = potions_display
        return context