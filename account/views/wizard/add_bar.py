from django.views.generic import TemplateView

from cheers.apps.bar.views.bar_add_new import ViewBarAdd


class ViewAccountWizardAddBar(ViewBarAdd):
    template_name = "account/wizard/add-bar.html"