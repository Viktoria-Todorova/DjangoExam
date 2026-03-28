from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)