from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from leads.models import Agent
from .forms import AgentModelForm
# Create your views here.


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreatView(LoginRequiredMixin, generic.CreateView):
    template_name = 'agents/create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent_list')

    def form_valid(self, form):
        agent = form.save(commit=False)
        # print(dir(self.request.user))

        agent.organisation = self.request.user.userprofile
        agent.save()

        return super(AgentCreatView, self).form_valid(form)


class AgentDetailView(generic.DetailView):
    template_name = 'agents/details.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(generic.UpdateView):
    template_name = 'agents/update.html'
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agent_list')


class AgentDeleteView(generic.DeleteView):
    template_name = 'agents/delete.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agent_list')
