from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Level, Attempt
# from .forms import CreateHabitForm, LogHabitForm

# Create your views here.

def main(request):
    return HttpResponse('kl20')

def Level(request, id):
    thislevel = Level.objects.filter(id=id)
    