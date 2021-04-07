from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin


class IsOrganiserAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organiser."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organiser:
            return redirect(reverse('leads:leads_list'))
        return super().dispatch(request, *args, **kwargs)
