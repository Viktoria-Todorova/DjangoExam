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

class BooksForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['title', 'writer', 'genre','quantity']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book Title ....'}),
            'writer': forms.TextInput(attrs={'placeholder': 'Writer ....'}),
            'genre': forms.Select(attrs={'placeholder': 'Genre ....'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Book Quantity ....'}),
        }

class DeleteBookForm(BooksForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True
