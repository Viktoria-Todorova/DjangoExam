from django import forms
from django.contrib.auth import get_user_model

from users.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'phone_number',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your username magician...'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Enter your password magician...'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '888 123 456',
                'maxlength': '10'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'
#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'placeholder': 'Enter your Username magician....',
#             }),
#             'first_name': forms.TextInput(attrs={
#                 'placeholder': 'Enter your first name'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'placeholder': 'Enter your last name'
#             }),
#             'phone_number': forms.TextInput(attrs={'placeholder': '888 123 456','maxlength': '10'},)
#             ,
#             'email': forms.EmailInput(attrs={
#                 'placeholder': 'your.email@example.com'
#             }),
#         }

UserModel = get_user_model()

class ProfileEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Confirm Password")

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

