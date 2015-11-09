from django.contrib import admin
from eve.models import MarketOrder, MarketHistory

admin.site.register(MarketOrder)
admin.site.register(MarketHistory)
