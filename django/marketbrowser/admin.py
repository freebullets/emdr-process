from django.contrib import admin
from common.models import MarketOrder, MarketHistory

admin.site.register(MarketOrder)
admin.site.register(MarketHistory)
