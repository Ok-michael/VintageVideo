from django.contrib import admin

from .models import Platform, Game, PriceList

admin.autodiscover()

admin.site.register(Platform)
admin.site.register(Game)
admin.site.register(PriceList)