from django import forms

class SearchForm(forms.Form):
    book_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search book by name ....'}),
    )