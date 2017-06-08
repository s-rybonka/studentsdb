from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'site_/home.html'


class TeamPageView(TemplateView):
    template_name = 'site_/team.html'