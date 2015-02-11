from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from eve.models import Type, Region, MarketOrder, MarketHistory
import json

def index(request):
    context = {
        'detail': 'active',
    }
    return render(request, 'marketbrowser/index.html', context)

def detail(request, region_id, type_id):
    orders = MarketOrder.objects.select_related('stationid', 'solarsystemid', 'typeid', 'regionid').filter(typeid=type_id, regionid=region_id)
    sells = sorted([i for i in orders if i.bid == False], key=lambda k: k.price)
    buys = sorted([i for i in orders if i.bid == True], key=lambda k: k.price, reverse=True)
    context = {
        'region': (sells and sells[0].regionid) or (buys and buys[0].regionid) or Region.objects.get(pk=region_id),
        'type': (sells and sells[0].typeid) or (buys and buys[0].typeid) or Type.objects.get(pk=type_id),
        'sells': sells,
        'buys': buys,
        'freshness': (sells and sells[0].generationdate) or (buys and buys[0].generationdate),
        'detail': 'active',
    }
    return render(request, 'marketbrowser/detail.html', RequestContext(request, context))

def arbitrage_index(request):
    context = {
        'arbitrage': 'active',
    }
    return render(request, 'marketbrowser/arbitrage_index.html', RequestContext(request, context))

def arbitrage(request, from_region_id, to_region_id):
    context = {
        'arbitrage': 'active',
    }
    return render(request, 'marketbrowser/arbitrage.html', RequestContext(request, context))

def autocomplete_item(request):
    data = Type.objects.filter(typename__istartswith=request.GET.get('q', '')).exclude(marketgroupid__isnull=True).order_by('typename').select_related('marketgroupid').values('typeid', 'typename', 'marketgroupid__marketgroupname')[:5]
    return HttpResponse(json.dumps(list(data)), content_type="application/json")