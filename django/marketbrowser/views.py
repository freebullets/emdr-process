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
    return render(request, 'marketbrowser/detail.html', context)

def arbitrage_index(request):
    sql = """
SELECT
    forge.typeID,
    invTypes.typeName,
    MIN(citadel.price) citadelSell,
    SUM(citadel.volRemaining) citadelUnits,
    MAX(forge.price) forgeBuy,
    SUM(forge.volRemaining) forgeUnits,
    ((MAX(forge.price) - MIN(citadel.price)) * LEAST(SUM(citadel.volRemaining), SUM(forge.volRemaining))) profit,
    ABS(TIMESTAMPDIFF(HOUR, MAX(forge.generationDate), MAX(citadel.generationDate))) dateDiff
FROM `marketOrders` forge 
INNER JOIN `marketOrders` citadel
    ON citadel.typeID = forge.typeID
INNER JOIN invTypes 
    ON forge.typeID=invTypes.typeID
WHERE forge.regionID = 10000002 AND forge.bid = 1
    AND citadel.regionID = 10000033 AND citadel.bid = 0
    AND citadel.price < forge.price
    AND forge.minVolume = 1
    AND ABS(TIMESTAMPDIFF(HOUR, forge.generationDate, citadel.generationDate)) < 24 
GROUP BY forge.typeID, invTypes.typeName
ORDER BY profit DESC
LIMIT 10
"""
    result = Type.objects.raw(sql, [])
    context = {
        'result': result,
        'arbitrage': 'active',
    }
    return render(request, 'marketbrowser/arbitrage_index.html', context)

def arbitrage(request, from_region_id, to_region_id):
    context = {
        'arbitrage': 'active',
    }
    return render(request, 'marketbrowser/arbitrage.html', context)

def autocomplete_item(request):
    data = Type.objects.filter(typename__istartswith=request.GET.get('q', '')).exclude(marketgroupid__isnull=True).order_by('typename').select_related('marketgroupid').values('typeid', 'typename', 'marketgroupid__marketgroupname')[:5]
    return HttpResponse(json.dumps(list(data)), content_type="application/json")