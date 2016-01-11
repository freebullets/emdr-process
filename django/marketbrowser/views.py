from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from common.models import Type, Region, MarketOrder, MarketHistory
from django.db.models import Count, Avg, Max, Min
import json

def index(request):
    context = {}
    return render(request, 'marketbrowser/index.html', context)

def snapshot_index(request):
    context = {
        'snapshot': 'active',
    }
    return render(request, 'marketbrowser/snapshot_index.html', context)

def snapshot_detail(request, region_id, type_id):
    orders = MarketOrder.objects.select_related('stationid', 'solarsystemid', 'typeid', 'regionid').filter(typeid=type_id, regionid=region_id)
    sells = sorted([i for i in orders if i.bid == False], key=lambda k: k.price)
    buys = sorted([i for i in orders if i.bid == True], key=lambda k: k.price, reverse=True)
    context = {
        'region': (sells and sells[0].regionid) or (buys and buys[0].regionid) or Region.objects.get(pk=region_id),
        'type': (sells and sells[0].typeid) or (buys and buys[0].typeid) or Type.objects.get(pk=type_id),
        'sells': sells,
        'buys': buys,
        'freshness': (sells and sells[0].generationdate) or (buys and buys[0].generationdate),
        'snapshot': 'active',
    }
    return render(request, 'marketbrowser/snapshot_detail.html', context)

def arbitrage_index(request):
    sql = """
SELECT
    invTypes.typeID,
    invTypes.typeName,
    MIN(citadel.price) citadelSell,
    SUM(citadel.volRemaining) citadelUnits,
    MAX(forge.price) forgeBuy,
    SUM(forge.volRemaining) forgeUnits,
    ((MAX(forge.price) - MIN(citadel.price)) * LEAST(SUM(citadel.volRemaining), SUM(forge.volRemaining))) profit,
    ABS(TIMESTAMPDIFF(MINUTE, MAX(forge.generationDate), MAX(citadel.generationDate))) dateDiff,
    forge.regionID forgeRegion,
    citadel.regionID citadelRegion
FROM invTypes
INNER JOIN `marketOrders` citadel
    ON citadel.typeID = invTypes.typeID
    AND citadel.regionID = 10000033 AND citadel.bid = 0
INNER JOIN `marketOrders` forge
    ON forge.typeID = invTypes.typeID
    AND forge.regionID = 10000002 AND forge.bid = 1
    AND forge.minVolume = 1
WHERE citadel.price < forge.price
    AND ABS(TIMESTAMPDIFF(MINUTE, forge.generationDate, citadel.generationDate)) < 240
GROUP BY invTypes.typeID, invTypes.typeName
ORDER BY profit DESC
LIMIT 25
"""
    result = Type.objects.raw(sql, [])
    context = {
        'result': result,
        'arbitrage': 'active',
    }
    return render(request, 'marketbrowser/arbitrage_index.html', context)

def arbitrage_detail(request, from_region_id, to_region_id):
    context = {
        'arbitrage': 'active',
    }
    return render(request, 'marketbrowser/arbitrage_detail.html', context)

def manufacturing_index(request):
    sql = """
SELECT prodTypeID typeID, prodTypeName, prodPrice, SUM(matPrice) matPrice, prodPrice-SUM(matPrice) profit, 24/volume marketVol, (prodPrice-SUM(matPrice))/GREATEST(time/60/60, 24/volume) iph FROM (
    SELECT prodType.typeID prodTypeID, prodType.typeName prodTypeName, prod.quantity prodQty, matType.typeName matTypeName, mat.quantity matQty, MIN(matOrder.price) minPrice, COALESCE(MIN(matOrder.price)*mat.quantity, 100000000000) matPrice, MIN(prodOrder.price)*prod.quantity prodPrice, COALESCE(attr.valueInt, attr.valueFloat) attrVal, ia.time time
    FROM industryActivityMaterials mat
    INNER JOIN industryActivityProducts prod
        ON mat.typeID=prod.typeID
    LEFT JOIN marketOrders matOrder
        ON mat.materialTypeID=matOrder.typeID
        AND matOrder.bid=0
        AND matOrder.regionID=10000002
    INNER JOIN marketOrders prodOrder
        ON prod.productTypeID=prodOrder.typeID
        AND prodOrder.bid=0
        AND prodOrder.regionID=10000002
    INNER JOIN invTypes matType
        ON mat.materialTypeID=matType.typeID
    INNER JOIN invTypes prodType
        ON prod.productTypeID=prodType.typeID
    LEFT JOIN dgmTypeAttributes attr
        ON prod.productTypeID=attr.typeID
        AND attr.attributeID=633
    INNER JOIN industryActivity ia
        ON mat.typeID=ia.typeID AND ia.activityID=1
    WHERE mat.activityID = 1
        AND (attr.valueInt = 0 OR attr.valueFloat = 0)
    GROUP BY mat.typeID, mat.materialTypeID
) materialList
INNER JOIN (
    SELECT SUM(quantity)/30 AS volume, typeID
    FROM marketHistory
    WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    AND regionID=10000002
    GROUP BY typeID
) history ON prodTypeID=history.typeID
WHERE 24/volume < 24
GROUP BY typeID
ORDER BY iph DESC
LIMIT 100
"""
    result = Type.objects.raw(sql, [])
    context = {
        'result': result,
        'manufacturing': 'active',
    }
    return render(request, 'marketbrowser/manufacturing_index.html', context)

def stats(request):
    items = Type.objects.all().filter(marketgroupid__isnull=False).aggregate(Count("typeid", distinct=True))
    market_items = MarketOrder.objects.all().aggregate(Count("typeid", distinct=True))
    from django.db import connection
    import datetime
    cursor = connection.cursor()
    cursor.execute("SELECT AVG(UNIX_TIMESTAMP(generationdate)) as avgdate FROM marketOrders WHERE regionID=10000002")
    row = cursor.fetchone()
    freshness = datetime.datetime.fromtimestamp(int(row[0]))
    context = {
        'stats': 'active',
        'items': items,
        'market_items': market_items,
        'freshness': freshness
    }
    return render(request, 'marketbrowser/stats.html', context)

def autocomplete_item(request):
    data = Type.objects.filter(typename__istartswith=request.GET.get('q', '')).exclude(marketgroupid__isnull=True).order_by('typename').select_related('marketgroupid').values('typeid', 'typename', 'marketgroupid__marketgroupname')[:5]
    return HttpResponse(json.dumps(list(data)), content_type="application/json")
