from django import forms

from potions.choices import HERB_CHOICES, LIQUID_CHOICES, ITEM_CHOICES
from users.models import User


class CreatePotionForm(forms.Form):

    magician = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter Username..."}),
    )
    herb = forms.ChoiceField(choices=HERB_CHOICES)
    liquid = forms.ChoiceField(choices=LIQUID_CHOICES)
    item = forms.ChoiceField(choices=ITEM_CHOICES)

    def clean_magician(self):
        username = self.cleaned_data["magician"]

        try:
            magician = User.objects.get(username=username)
            return magician
        except User.DoesNotExist:
            raise forms.ValidationError('No magician with this username exists!')

# class PotionFilterForm(forms.Form):