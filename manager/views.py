from django.shortcuts import render
from django.views.generic import TemplateView
from utils.mixins import ManagerRequiredMixin


class MainView(ManagerRequiredMixin, TemplateView):
    template_name = 'manager/main_page.html'
