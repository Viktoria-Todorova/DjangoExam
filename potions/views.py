from django.shortcuts import render

import random
from django.shortcuts import render
from .forms import CreatePotionForm

SUCCESS_POTIONS = [
    "Potion of Healing",
    "Potion of Invisibility",
    "Potion of Sweet Dreams",
    "Potion of Fire Resistance",
]

FAIL_POTIONS = [
    "Potion of Exploding Frogs 🐸💥",
    "Potion of Endless Sneezing 🤧",
    "Potion of Pink Smoke 💨",
    "Potion of Hair Growth (Everywhere)",
]

def create_potion(request):
    result = None
    potion_name = None

    if request.method == "POST":
        form = CreatePotionForm(request.POST)

        if form.is_valid():
            herb = form.cleaned_data["herb"]
            liquid = form.cleaned_data["liquid"]
            item = form.cleaned_data["item"]

            # MAGIC RULE (you can invent your own!)
            if herb == "lavender" and liquid == "milk":
                result = "success"
                potion_name = random.choice(SUCCESS_POTIONS)
            else:
                result = "fail"
                potion_name = random.choice(FAIL_POTIONS)

    else:
        form = CreatePotionForm()

    return render(request, "potions/create-potions.html", {
        "form": form,
        "result": result,
        "potion_name": potion_name
    })
