from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ViewAccountDashboard(LoginRequiredMixin, TemplateView):
    template_name = "account/dashboard.html"