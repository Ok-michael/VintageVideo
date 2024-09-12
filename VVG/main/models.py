from django.db import models

class Platform(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class GameManager(models.Manager):
    def get_promoted(self):
        return self.filter(promoted=True)
    
    def get_unpromoted(self):
        return self.filter(promoted=False)
    
    def get_platform(self, platform):
        return self.filter(platform__name__iexact=platform)


class Game(models.Model):
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