from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Lead, Agent, Category

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
            'agent',
            'phone_number',
            'email',
            'description',
        )


class LeadForm(forms.Form):

    first_name = forms.CharField(label='First name..', max_length=100)
    last_name = forms.CharField(label='Last name..', max_length=100)
    age = forms.IntegerField(min_value=0, max_value=140)


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    # this is done so that we can access the request object in the
    # form here which is passed as context from the view
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('request').user
        agents = Agent.objects.filter(organisation=user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = (
            'category',
        )
