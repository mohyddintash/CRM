from django.forms import ModelForm

from leads.models import Agent


class AgentModelForm(ModelForm):
    class Meta:
        model = Agent
        fields = (
            'user',
        )
