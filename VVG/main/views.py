from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm
from django.contrib.auth.models import User
from .models import Game


def index(request):
    max_promoted_games = 3
    max_games_list = 6
    promoted_games_list = Game.objects.get_promoted()
    games_list = Game.objects.get_unpromoted()
    
    show_more_link_promoted = promoted_games_list.count() > max_promoted_games
    show_more_link_games = games_list.count() > max_games_list
    
    context = {
        'promoted_games_list': promoted_games_list[:max_promoted_games],
        'games_list': games_list[:max_games_list],
        'show_more_link_promoted': show_more_link_promoted,
        'show_more_link_games': show_more_link_games
    }
    return render(request, 'main/index.html', context)


def show_all_games(request):
    games = Game.objects.all()
    context = {'games': games}
    return render(request, 'main/all_games.html', context)


def show_promoted_games(request):
    games = Game.objects.get_promoted()
    context = {'games': games}
    return render(request, 'main/promoted.html', context)
    

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username  = form.cleaned_data['username'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            )
            user.save()
            return render(request, 'main/successful_registration.html', {})
    form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})