from django import forms


class LoginForm(forms.Form):
    magician = forms.CharField(max_length=100)