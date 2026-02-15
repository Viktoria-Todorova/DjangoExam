from django import forms

from users.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '08888888',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com'
            }),
        }
