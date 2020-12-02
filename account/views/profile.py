from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from cheers.apps.account.forms.profile import FormAccountProfile
from cheers.apps.account.models import ModelAccountUser


class ViewAccountProfile(SuccessMessageMixin, UpdateView):

    model = ModelAccountUser
    template_name = "account/profile.html"
    success_url = reverse_lazy("account:profile")
    form_class = FormAccountProfile
    success_message = "Your Profile updated successfully"

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)