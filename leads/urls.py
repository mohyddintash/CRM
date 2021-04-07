from django.urls import path

from .views import (LeadsList, LeadDetails, LeadCreate,
                    LeadUpdate, LeadDelete, AssignAgentView, CategoryListView, CategoryDetailsView, CategoryUpdate)

app_name = 'leads'

urlpatterns = [
    path('', LeadsList.as_view(), name='leads_list'),
    path('create/', LeadCreate.as_view(), name='lead_create'),
    path('<int:pk>/', LeadDetails.as_view(), name='lead_details'),
    path('<int:pk>/update/', LeadUpdate.as_view(), name='lead_update'),
    path('<int:pk>/delete/', LeadDelete.as_view(), name='lead_delete'),
    path('<int:pk>/update-category/',
         CategoryUpdate.as_view(), name='lead_category_update'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign_agent'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailsView.as_view(),
         name='category_details'),
]
