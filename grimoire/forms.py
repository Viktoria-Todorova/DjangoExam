from django import forms

from grimoire.models import Grimoire


class GrimoireForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput())
    class Meta:
        model = Grimoire
        fields = ['body','magician', 'type_of_story', 'image']
        labels ={
            'body':''
        }

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