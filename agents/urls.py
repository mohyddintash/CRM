from django.urls import path

from .views import AgentListView, AgentCreatView, AgentDetailView, AgentUpdateView, AgentDeleteView

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent_list'),
    path('<int:pk>/', AgentDetailView.as_view(), name='agent_details'),
    path('create/', AgentCreatView.as_view(), name='agent_create'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent_update'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent_delete'),
]
