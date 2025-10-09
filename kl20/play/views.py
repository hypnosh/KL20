from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Level, Attempt, Player
from .forms import AnswerForm, LoginForm

# Create your views here.

def main(request):
    if not request.session.get('player_id'):
        return HttpResponse('/login/')

    player = Player.objects.filter(id=request.session.get('player_id'))
    if not player:
        del request.session['player_id']
        return HttpResponseRedirect('/login/')
    player = player[0]
    return HttpResponseRedirect(f'/level/{player.last_level.id if player.last_level else 1}/')

def Login(request):
    if request.session.get('player_id'):
        return HttpResponseRedirect('/')

    template = loader.get_template('login.html')
    form = LoginForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            player = Player.objects.filter(email=email, password=password)
            if player:
                player = player[0]
                request.session['player_id'] = player.id
                return HttpResponseRedirect('/')
            else:
                context['error'] = 'Invalid email or password'
    
    return HttpResponse(template.render(context, request))

def Logout(request):
    if request.session.get('player_id'):
        del request.session['player_id']
    return HttpResponseRedirect('/login/') 

def LevelView(request, slug='', id=0):

    if slug:
        thislevel = Level.objects.filter(slug=slug)
    elif id:
        thislevel = Level.objects.filter(id=id)
    
    if not thislevel:
        return HttpResponse('No such level')
    thislevel = thislevel[0]

    # breakpoint()
    # check user's last level
    if request.session.get('player_id'):
        player = Player.objects.filter(id=request.session.get('player_id'))
        if player:
            player = player[0]

            if request.method == "POST":
                form = AnswerForm(request.POST)
                if form.is_valid():
                    answer = form.cleaned_data['answer']
                    correct = (answer.strip().lower() == thislevel.answer.strip().lower())
                    Attempt.objects.create(level=thislevel, answer=answer, correct=correct, player=player)
                    if correct:
                        # if correct, redirect to next level
                        next_level = Level.objects.filter(id=int(thislevel.id)+1) # get it from a query
                        if next_level:
                            return HttpResponseRedirect(f'/level/{next_level[0].id}/')
                        else:
                            return HttpResponse('Congratulations! You have completed all levels.')
                    else:
                        # route parsing from json
                        context = {
                            'level': thislevel,
                            'form': form,
                            'error': 'Incorrect answer. Please try again.'
                        }
                        template = loader.get_template('level.html')
                        return HttpResponse(template.render(context, request))
            else: # if get
            # now do all of the logic building
            # 	fetch last level
            # 	if last > current - go to last
            #	if last < current
            #		checkpoint between last and current?
            #		if checkpoint exists - go to checkpoint
            #		if checkpoint doesn't exist - render current, set current as last
            if 1==0:
                if player.last_level and int(player.last_level.id) + 1 > int(thislevel.id):
                    # redirect to last level - this level < player level
                    return HttpResponseRedirect(f'/level/{player.last_level.id}/')
                elif int(thislevel.id) > 1 and (not player.last_level or int(player.last_level.id) + 1 < int(thislevel.id)):
                    # redirect to last level - this level > player level + 1
                    # fetch last checkpoint level
                    checkpoint_level = Level.objects.filter(checkpoint=True, id__lt=player.last_level.id).order_by('-id')
                    # if checkpoint level exists and is less than this level, redirect to it
                    if checkpoint_level < thislevel.id:
                        return HttpResponseRedirect(f'/level/{checkpoint_level[0].id}/')
                    last_level_id = player.last_level.id if player.last_level else 1
                    return HttpResponseRedirect(f'/level/{last_level_id}/')
        else:
            del request.session['player_id']
            return HttpResponseRedirect('/login/')
    # breakpoint()
    template = loader.get_template('level.html')
    form = AnswerForm()
    context = {
        'level': thislevel,
        'form': form,
    }
    # set session level id
    request.session['level_id'] = thislevel.id
    # set player's last level to this level if not set
    if request.session.get('player_id') and (not player.last_level or int(player.last_level.id) < int(thislevel.id)):
        player.last_level = thislevel
        player.save()

    return HttpResponse(template.render(context, request))