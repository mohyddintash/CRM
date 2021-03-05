from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Lead

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class LeadModelForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent'
        )


class LeadForm(forms.Form):

    first_name = forms.CharField(label='First name..', max_length=100)
    last_name = forms.CharField(label='Last name..', max_length=100)
    age = forms.IntegerField(min_value=0, max_value=140)
