from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=30)
    phone = forms.IntegerField()

    class Meta:
        model = Account
        fields = ('email','name','phone','password1','password2')
        