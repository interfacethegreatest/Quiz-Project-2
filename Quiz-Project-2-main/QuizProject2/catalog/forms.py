from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.apps import apps
from .models import Order, UserProfile


class OrderForm(ModelForm):
    class Meta:
        model = Order 
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username','email', 'password1', 'password2', 'first_name', 'last_name']