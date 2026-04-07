from django import forms

from grimoire.models import Grimoire
from grimoire.validators import FileSizeValidator


class GrimoireForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(), validators=[FileSizeValidator(5)])

    class Meta:
        model = Grimoire
        fields = ['body', 'type_of_story', 'image']
        labels = {'body': ''}



class DeleteGrimoireForm(forms.ModelForm):
    class Meta:
        model = Grimoire
        exclude = ['created_at','image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True