from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, ObservationPoint
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    username=forms.CharField(required=True, label="Nazwa użytkownika")
    first_name=forms.CharField(required=True, max_length=20, label="Imię")
    last_name=forms.CharField(required=True, max_length=30,label="Nazwisko")
    email=forms.EmailField(required=True,label="Adres e-mail")

    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email','password1','password2']


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        required=True,
        label="Adres e-mail",
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500",
            "placeholder": "Wprowadź adres e-mail"
        })
    )

    password = forms.CharField(
        required=True,
        label="Hasło",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500",
            "placeholder": "Wprowadź hasło"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user_object = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Adres e-mail lub hasło nie są prawidłowe")

            user = authenticate(username=user_object.email, password=password)
            if user is None:
                raise forms.ValidationError("Adres e-mail lub hasło nie są prawidłowe")

            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user

class ObservationPointForm(forms.ModelForm):
    class Meta:
        model=ObservationPoint
        fields=['title','description','latitude','longitude','energyCostPerKWh']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'title': 'Nazwa lokalizacji',
            'description': 'Opis',
            'latitude': 'Szerokość geograficzna',
            'longitude': 'Długość geograficzna',
            'energyCostPerKWh':"Koszt energii elektrycznej na KWh"
        }

#formularz do aktualizacji username, first name oraz last name
class UpdateUserUFLNameForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name']
        labels = {
            'username': 'Nazwa użytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko'
        }

