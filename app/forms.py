from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Customer.objects.create(
                user=user,
            )
        return user