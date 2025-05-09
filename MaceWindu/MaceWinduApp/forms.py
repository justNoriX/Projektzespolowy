from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    username=forms.CharField(required=True, label="Username")
    first_name=forms.CharField(required=True, max_length=20, label="First name")
    last_name=forms.CharField(required=True, max_length=30,label="Last name")
    email=forms.EmailField(required=True,label="Email address")

    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email','password1','password2']


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args,**kwargs)

    email = forms.EmailField(required=True, label="Email address")
    password=forms.CharField(required=True,label="Password",widget=forms.PasswordInput)
    def clean(self):
        cleaned_data=super().clean()
        email=cleaned_data.get('email')
        password=cleaned_data.get('password')

        if email and password:
            try:
                user_object=CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Email or password not valid!")
            user=authenticate(username=user_object.email,password=password)
            if user is None:
                raise forms.ValidationError("Email or password not valid!")
            self.user=user
        return cleaned_data
    def get_user(self):
        return self.user
