from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, reverse
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Lead, Agent

from .forms import LeadForm, LeadModelForm, SignupForm


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def get_success_url(self):
        return reverse('login')

# Class based Views


class LandingPage(generic.TemplateView):
    template_name = 'landing.html'


class LeadsList(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/list.html'
    queryset = Lead.objects.all()
    context_object_name = 'leads'  # defailt name of context for ListView is object_list


class LeadDetails(generic.DetailView):
    template_name = 'leads/details.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


class LeadCreate(generic.CreateView):
    template_name = 'leads/create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:leads_list')

    def form_valid(self, form):
        # TODO send email on creation
        send_mail(
            subject='A lead has been created', message='Go to the site to see te new lead.',
            from_email='mo@crmtest.com', recipient_list=['test2@test.com']
        )
        return super(LeadCreate, self).form_valid(form)


class LeadUpdate(generic.UpdateView):
    template_name = 'leads/update.html'
    form_class = LeadModelForm
    queryset = Lead.objects.all()
    context_object_name = 'lead'

    def get_success_url(self):
        return reverse('leads:leads_list')


class LeadDelete(generic.DeleteView):
    template_name = 'leads/delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:leads_list')

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
