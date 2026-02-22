from django import forms

from grimoire.models import Grimoire
from users.models import User


class GrimoireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['magician'] = ''
        # self.data = self.data.copy()

    image = forms.ImageField(required=False, widget=forms.FileInput())
    magician = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter Username..."}),
    )
    class Meta:
        model = Grimoire
        fields = ['body', 'type_of_story', 'image']
        labels ={
            'body':''
        }

    def clean_magician(self):
        username = self.cleaned_data["magician"]
        try:
            magician = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('No magician with this username exists!')

        if self.instance and self.instance.magician != magician:
            raise forms.ValidationError('You are not the owner of this grimoire!You are not supposed to touch this')

        return magician

#todo when we are able to do logins only the current user to be able to delete it
class DeleteGrimoireForm(forms.ModelForm):
    class Meta:
        model = Grimoire
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True