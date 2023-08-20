from django.shortcuts import render
from django.views import View, generic
from django.utils import timezone


class homepage(generic.TemplateView):
    template_name = 'home/homepage.html'
