from django.db import models
from django.contrib.auth.models import User
from collections import namedtuple


class Platform(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class GameManager(models.Manager):
    """ This class implements some methods used for managing
    the Game class. I create no table in the database but simply
    adds functionalitie to out Game class

    Args:
        models (models.Manager): This is django native class
        from which this class inherits
    """
    def get_promoted(self):
        return self.filter(promoted=True)
    
    def get_unpromoted(self):
        return self.filter(promoted=False)
    
    def get_platform(self, platform):
        return self.filter(platform__name__iexact=platform)


class Game(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    class Meta:
        ordering = ['-promoted', 'name']
    
    objects = GameManager()
    
    name = models.CharField(max_length=100)
    release_year = models.IntegerField(null=True)
    developer = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='images/',
        default='images/placeholder.png',
        max_length=100
    )
    platform = models.ForeignKey(
        Platform, null=False, on_delete=models.CASCADE
    )
    promoted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.platform} - {self.name}'
    

class PriceList(models.Model):
    """This is the class that models the Pricelist table
    in our database. It inherits from models.Model

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    game = models.OneToOneField(
        Game, on_delete=models.CASCADE, primary_key=True
    ) 
    price_per_unit = models.DecimalField(
        max_digits=9, decimal_places=2, default=0
    )
    add_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.game.name
    

class ShoppingCartManager(models.Manager):
    """ This class implements three simple methods used to manage
    our ShoppingCart model. I doesn't directly create any table in
    the database but simply supports some functionalities in
    ShoppingCart

    Args:
        models (_type_): this is the model.Manager class use to
        manage our ShoppingCart class
    """
    def get_id(self, id):
        return self.get(pk=id)
    
    def get_user(self, user):
        return self.get(user_id=user.id)
    
    def create_cart(self, user):
        new_cart = self.create(user=user)
        return new_cart
    
    def empty(self, cart): 
        cart_items = ShoppingCartItem.objects.filter( 
            cart__id=cart.id 
        ) 
        for item in cart_items: 
            item.delete()

    

class ShoppingCart(models.Model):
    objects=ShoppingCartManager()
    user = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username}'s shopping cart"
    
class ShoppingCartItemManager(models.Manager):
    def get_items(self, cart):
        return self.filter(cart_id=cart.id)
    
    def get_existing_item(self, cart, game):
        try:
            return self.get(cart_id=cart.id, game_id=game.id)
        except ShoppingCartItem.DoesNotExist:
            return None
    

class ShoppingCartItem(models.Model):
    objects = ShoppingCartItemManager()
    quantity = models.IntegerField(null=False)
    price_per_unit = models.DecimalField(
        max_digits=9, decimal_places=2, default=0
    )
    cart = models.ForeignKey(
        ShoppingCart, null=False, on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game, null=False, on_delete=models.CASCADE
    )

OrderItem = namedtuple('OrderItem', 'name price_per_unit product_id quantity')
