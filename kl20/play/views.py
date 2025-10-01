from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Level, Attempt
from .forms import AnswerForm, LoginForm
# from .forms import CreateHabitForm, LogHabitForm

# Create your views here.

def main(request):
    return HttpResponse('kl20')

def Level(request, id):
    thislevel = Level.objects.filter(id=id)
    if not thislevel:
        return HttpResponse('No such level')
    thislevel = thislevel[0]
    template = loader.get_template('level.html')
    form = AnswerForm()
    context = {
        'level': thislevel,
        'form': form,
    }
    return HttpResponse(template.render(context, request))