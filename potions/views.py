import random

from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from .forms import CreatePotionForm
from .models import Potion, SecretPotions

POTION_RECIPES = {
    ("lavender", "milk", "feather"): "Potion of Sweet Dreams",
    ("mint", "water", "crystal"): "Potion of Healing",
    ("sage", "water", "pearl"): "Potion of Clarity",
    ("chamomile", "honey", "dust"): "Potion of Calm Mind",
    ("aloe", "water", "ice_shard"): "Potion of Cooling Skin",
    ("nightshade", "oil", "shadow_dust"): "Potion of Invisibility",
    ("sunflower", "alcohol", "gold_flake"): "Potion of Radiance",
    ("lotus", "water", "moonstone"): "Potion of Water Breathing",
    ("ginger_root", "fire_water", "ash"): "Potion of Fire Resistance",
    ("blue_orchid", "ether", "butterfly_wing"): "Potion of Levitation",
    ("thorn_leaf", "blood", "iron"): "Potion of Strength",
    ("wolf_fang", "oil", "bone_fragment"): "Potion of Rage",
    ("frost_berry", "ice_water", "silver"): "Potion of Frost Armor",
    ("ember_leaf", "alcohol", "dragon_scale"): "Potion of Flame Aura",
    ("nettle", "vinegar", "spider_silk"): "Potion of Poison Touch",
    ("moonflower", "dew", "stardust"): "Potion of Time Slow",
    ("black_rose", "ink", "crow_feather"): "Potion of Shadow Walk",
    ("ghost_mushroom", "fog", "spirit_essence"): "Potion of Spirit Form",
    ("crystal_rose", "holy_water", "opal"): "Potion of Purification",
    ("mandrake", "elixir", "ancient_coin"): "Potion of Memory Recall",
    ("void_root", "tar", "obsidian"): "Potion of Darkness",
    ("blood_lily", "blood", "heart_fragment"): "Potion of Life Drain",
    ("wyrm_scale", "lava", "ruby"): "Potion of Dragon Breath",
    ("time_sand", "mercury", "clock_gear"): "Potion of Time Reversal",
    ("star_tear", "liquid_light", "halo_fragment"): "Potion of Ascension",
}


FAIL_POTIONS = [
    "Potion of Exploding Frogs 🐸💥",
    "Potion of Endless Sneezing 🤧",
    "Potion of Pink Smoke 💨",
    "Potion of Hair Growth (Everywhere)",
    "Potion of Temporary Chicken Language 🐔",
    "Potion of Uncontrollable Dancing 💃",
    "Potion of Invisible Socks",
    "Potion of Loud Thoughts 🔊",
    "Potion of Gravity Confusion",
    "Potion of Beard Multiplication 🧔🧔🧔",
]

class CreatePotionView(FormView):
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
        magician = form.cleaned_data["magician"]
        ingredients = (herb, liquid, item)

        if ingredients in POTION_RECIPES:
            potion_name = POTION_RECIPES[ingredients]
            result = "success"

            Potion.objects.get_or_create(
                name=potion_name,
                magician=magician,
                defaults={"description": f"Brewed with {herb}, {liquid}, and {item}."}
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
