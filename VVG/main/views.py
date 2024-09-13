from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm
from django.contrib.auth.models import User
from .models import Game
from django.views.generic.edit import UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Sum, F, DecimalField
from .models import ShoppingCart
from .models import ShoppingCartItem
from .forms import ShoppingCartFormSet
from decimal import Decimal


@login_required
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


class ShoppingCartEditView(UpdateView):
    model = ShoppingCart
    form_class = ShoppingCartFormSet
    template_name = 'main/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = ShoppingCartItem.objects.get_items(self.object)
        context['is_cart_empty'] = (items.count() == 0)
        order = items.aggregate(
            total_order=Sum(
                F('price_per_unit') * F('quantity'),
                output_field=DecimalField()
            )
        )
        context['total_order'] = order['total_order']
        return context
    
    def get_object(self):
        try:
            return ShoppingCart.objects.get_user(self.request.user)
        except ShoppingCart.DoesNotExist:
            new_cart = ShoppingCart.objects.create_cart(self.request.user)
            new_cart.save()
            return new_cart
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        return HttpResponseRedirect(reverse_lazy('user-cart'))
    

@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    cart = ShoppingCart.objects.get_user(request.user)
    existing_item = ShoppingCartItem.objects.get_existing_item(
        cart, game
    )
    if existing_item is None:
        price = (Decimal(0)) if not hasattr(
            game, 'pricelist') else game.pricelist.price_per_unit
        new_item = ShoppingCartItem(
            game=game, quantity=1, price_per_unit=price, cart=cart
        )
        new_item.save()
    else:
        existing_item.quantity = F('quantity') + 1
        existing_item.save()
        messages.add_message(
            request, 
            messages.INFO, 
            f'The game {game.name} has been added to your cart'
        )
    return HttpResponseRedirect(reverse_lazy('user-cart'))
