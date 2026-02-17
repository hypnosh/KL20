from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Level, Attempt, Player, Content
from .forms import AnswerForm, LoginForm

# Create your views here.

def main(request):
    if not request.session.get('player_id'):
        return HttpResponseRedirect('/login/')

    player = Player.objects.filter(id=request.session.get('player_id'))
    if not player:
        del request.session['player_id']
        return HttpResponseRedirect('/login/')
    player = player[0]
    return HttpResponseRedirect(f'/level/{player.last_level.id if player.last_level else 1}/')

def ContentView(request, slug):
    template = loader.get_template('cms.html')

    content = Content.objects.filter(slug=slug)
    if not content:
        return HttpResponse('Content not found')
    content = content[0]

    context = {
        'content': content,
    }
    return HttpResponse(template.render(context, request))

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

def GmailLogin(request):
    if request.session.get('player_id'):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        player = Player.objects.filter(email=email)
        if player:
            player = player[0]
        else:
            # create new player
            player = Player.objects.create(name=email.split('@')[0], email=email, password='gmail_oauth', is_admin=False)
        request.session['player_id'] = player.id
        return HttpResponseRedirect('/')

    return HttpResponseRedirect('/login/')

def Logout(request):
    if request.session.get('player_id'):
        del request.session['player_id']
    return HttpResponseRedirect('/login/') 


def LevelView(request, slug='', id=0):
    # Game logic resides in this view

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
                        next_level = Level.objects.filter(prev_level = thislevel)
                        # next_level = Level.objects.filter(id=int(thislevel.id)+1) # get it from a query
                        if next_level:
                            return HttpResponseRedirect(f'/level/{next_level[0].id}/')
                        else:
                            return HttpResponse('Congratulations! You have completed all levels.')
                    else:
                        # if not correct, route parsing from json
                        routes = thislevel.routes
                        if routes:
                            message = routes.get(answer.strip().upper())
                            if not message:
                                message = "Wrong!"
                        else:
                            message = "Wrong!"

                        context = {
                            'level': thislevel,
                            'form': form,
                            'error': message
                        }
                        template = loader.get_template('level.html')
                        return HttpResponse(template.render(context, request))
                        
            else: # if get
                # 	fetch last level
                last_level = player.last_level if player.last_level else 1
                if int(last_level.id) > int(thislevel.id):
                    # 	if last > current - go to last
                    return HttpResponseRedirect(f'/level/{last_level.id}/')
                else:
                    # if last < current
                    # breakpoint()
                    checkpoint_level = Level.objects.filter(checkpoint=True, id__lt=thislevel.id).order_by('-id')
                        # checkpoint between last and current?
                        # let's figure this out on 14th nov
                    if checkpoint_level and int(last_level.id) < int(checkpoint_level[0].id):
                        # if the checkpoint is after last level, i.e. the user has still not crossed the checkpoint
                        return HttpResponseRedirect(f'/level/{checkpoint_level[0].id}/')
                        # if checkpoint exists - go to checkpoint
                    else:
                        # else continue
                        pass
                player.last_level = thislevel
                player.save()
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