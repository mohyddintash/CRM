import random
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from leads.models import Agent
from .forms import AgentModelForm

from .mixins import IsOrganiserAndLoginRequiredMixin


class AgentListView(IsOrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreatView(IsOrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f'{random.random()*10000}')
        user.save()
        Agent.objects.create(
            user=user, organisation=self.request.user.userprofile)
        send_mail(
            subject='You are invited to be an agent',
            message='You are invited to be an agent in SystemCRM. Visit the site to login and setup your account.',
            from_email='admin@systemcrm.com',
            recipient_list=[user.email]
        )

        return super(AgentCreatView, self).form_valid(form)


class AgentDetailView(IsOrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/details.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(IsOrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/update.html'
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agent_list')


class AgentDeleteView(IsOrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/delete.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agent_list')
