from random import choices

from django import forms

from catalog.models import Catalog


class SearchForm(forms.Form):
    book_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search book by name ....'}),
    )

class GenreFilterForm(forms.Form):
    genre = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'onchange': 'this.form.submit()'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].choices = [('', 'All Genres')] + list(Catalog.Genre.choices)
