from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class PainelView(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'
