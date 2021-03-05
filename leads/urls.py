from django.urls import path

from .views import LeadsList, LeadDetails, LeadCreate, LeadUpdate, LeadDelete

app_name = 'leads'

urlpatterns = [
    path('', LeadsList.as_view(), name='leads_list'),
    path('<int:pk>/', LeadDetails.as_view(), name='lead_details'),
    path('create/', LeadCreate.as_view(), name='lead_create'),
    path('<int:pk>/update/', LeadUpdate.as_view(), name='lead_update'),
    path('<int:pk>/delete/', LeadDelete.as_view(), name='lead_delete'),
]
