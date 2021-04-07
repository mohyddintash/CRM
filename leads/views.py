from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, reverse
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Lead, Agent, Category
from .forms import LeadForm, LeadModelForm, SignupForm, AssignAgentForm, LeadCategoryUpdateForm

from agents.mixins import IsOrganiserAndLoginRequiredMixin

# Class based Views


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def get_success_url(self):
        return reverse('login')


class LandingPage(generic.TemplateView):
    template_name = 'landing.html'


class LeadsList(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/list.html'
    context_object_name = 'leads'  # defailt name of context for ListView is object_list

    def get_queryset(self):

        user = self.request.user
        # Lead.objects.filter(organisation__user=user)
        # initial queryset
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=False)
        else:
            # here we must be an agent but we still need to filter first for the agent's organisation
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadsList, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=True)
            context['unassigned_leads'] = queryset
        return context


class LeadDetails(generic.DetailView):
    template_name = 'leads/details.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        # initial queryset
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            # here we must be an agent but we still need to filter first for the agent's organisation
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreate(IsOrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:leads_list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        # TODO send email on creation
        send_mail(
            subject='A lead has been created', message='Go to the site to see te new lead.',
            from_email='mo@crmtest.com', recipient_list=['test2@test.com']
        )
        return super(LeadCreate, self).form_valid(form)


class LeadUpdate(IsOrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/update.html'
    form_class = LeadModelForm
    context_object_name = 'lead'

    def get_success_url(self):
        return reverse('leads:leads_list')

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)


class LeadDelete(IsOrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/delete.html'

    def get_success_url(self):
        return reverse('leads:leads_list')

    def get_queryset(self):
        user = self.request.user
        # initial queryset
        if user.is_organiser:
            return Lead.objects.filter(organisation=user.userprofile)


class AssignAgentView(IsOrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    # this passes the request object to the form class
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse('leads:leads_list')

    def form_valid(self, form):
        # form.save() doesn't work here because AssignAgentForm isn't a ModelForm.
        # However, it will work if we had a save method in AssignAgentForm class of course
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        user = self.request.user
        # initial queryset
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile)
        else:
            # here we must be an agent but we still need to filter first for the agent's organisation
            queryset = Category.objects.filter(
                organisation=user.agent.organisation)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        queryset = Lead.objects.filter(
            organisation=user.userprofile, category__isnull=True)
        context['uncategorized_count'] = queryset.count()
        return context


class CategoryDetailsView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_details.html'
    context_object_name = 'category'

    '''
    # this works but also in templates we could use category.lead_set.all which is cleaner to read
    # if we set related_name to something like leads for category field in the Lead models then we replace lead_set with leads
    # so that we can use category.leads
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailsView, self).get_context_data(**kwargs)
        context.update({
            'leads': self.get_object().lead_set.all()
        })
        return context
    '''

    def get_queryset(self):
        user = self.request.user
        # initial queryset
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            # here we must be an agent but we still need to filter first for the agent's organisation
            queryset = Category.objects.filter(
                organisation=user.agent.organisation)
        return queryset


class CategoryUpdate(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        # initial queryset
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            # here we must be an agent but we still need to filter first for the agent's organisation
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('leads:lead_category_update', kwargs={'pk': self.get_object().id})

# Same but using Function Based Views


def landing_page(request):
    return render(request, "landing.html")


def leads_list(request):
    context = {
        'leads': Lead.objects.all()
    }
    return render(request, "leads/list.html", context)


def lead_details(request, pk):
    context = {
        'lead': Lead.objects.get(pk=pk)
    }

    return render(request, "leads/details.html", context)


def lead_create(request):

    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/leads')

    else:
        form = LeadModelForm()

    return render(request, 'leads/create.html', {'form': form})


def lead_update(request, pk):

    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == 'POST':
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/leads')

    context = {
        'form': form,
        'lead': lead
    }

    return render(request, 'leads/update.html', context)


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

# Below are Less easy ways od doing Forms

# def lead_update(request, pk):

#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             first_name = data['first_name']
#             last_name = data['last_name']
#             age = data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return HttpResponseRedirect('/leads')

#     context = {
#         'form': form,
#         'lead': lead
#     }

#     return render(request, 'leads/update.html', context)


# def lead_create(request):

#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             first_name = data['first_name']
#             last_name = data['last_name']
#             age = data['age']
#             agent = Agent.objects.get(id=1)
#             lead = Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             return HttpResponseRedirect('/leads')

#     else:
#         form = LeadForm()

#     return render(request, 'leads/create.html', {'form': form})
