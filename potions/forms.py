from django import forms

class CreatePotionForm(forms.Form):
    HERB_CHOICES = [
        ("mint", "Mint"),
        ("lavender", "Lavender"),
        ("mushroom", "Glow Mushroom"),
        ("nettle", "Nettle"),
    ]

    LIQUID_CHOICES = [
        ("water", "Spring Water"),
        ("milk", "Moon Milk"),
        ("honey", "Honey Syrup"),
        ("ink", "Octopus Ink"),
    ]

    ITEM_CHOICES = [
        ("feather", "Phoenix Feather"),
        ("scale", "Dragon Scale"),
        ("bone", "Fairy Bone"),
        ("stone", "Moon Stone"),
    ]

    herb = forms.ChoiceField(choices=HERB_CHOICES)
    liquid = forms.ChoiceField(choices=LIQUID_CHOICES)
    item = forms.ChoiceField(choices=ITEM_CHOICES)
