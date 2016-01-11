# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

@python_2_unicode_compatible
class MarketGroup(models.Model):
    marketgroupid = models.IntegerField(db_column='marketGroupID', primary_key=True)
    parentgroupid = models.IntegerField(db_column='parentGroupID', blank=True, null=True)
    marketgroupname = models.CharField(db_column='marketGroupName', max_length=100, blank=True)
    description = models.CharField(max_length=3000, blank=True, null=True)
    iconid = models.IntegerField(db_column='iconID', blank=True, null=True)
    hastypes = models.IntegerField(db_column='hasTypes', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'invMarketGroups'
    def __str__(self):
        return self.marketgroupname

@python_2_unicode_compatible
class Type(models.Model):
    typeid = models.IntegerField(db_column='typeID', primary_key=True)
    groupid = models.IntegerField(db_column='groupID', blank=True, null=True)
    typename = models.CharField(db_column='typeName', max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    portionsize = models.IntegerField(db_column='portionSize', blank=True, null=True)
    raceid = models.SmallIntegerField(db_column='raceID', blank=True, null=True)
    baseprice = models.DecimalField(db_column='basePrice', max_digits=19, decimal_places=4, blank=True, null=True)
    published = models.IntegerField(blank=True, null=True)
    marketgroupid = models.ForeignKey(MarketGroup, db_column='marketGroupID', blank=True, null=True)
    iconid = models.BigIntegerField(db_column='iconID', blank=True, null=True)
    soundid = models.BigIntegerField(db_column='soundID', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'invTypes'
    def __str__(self):
        return self.typename

#@python_2_unicode_compatible
#class BlueprintMaterial(models.Model):
#    id = models.AutoField(primary_key=True)
#    typeid = models.ForeignKey(Type, db_column='typeID')
#    activityid = models.IntegerField(db_column='activityID')
#    materialtypeid = models.ForeignKey(Type, db_column='materialTypeID')
#    quantity = models.IntegerField(db_column='quantity')
#    class Meta:
#        managed = False
#        db_table = 'industryActivityMaterials'
#    def __str__(self):
#        return self.typeid.typename + " : " + self.materialtypeid.typename
#
#@python_2_unicode_compatible
#class BlueprintProduct(models.Model):
#    id = models.AutoField(primary_key=True)
#    typeid = models.ForeignKey(Type, db_column='typeID')
#    activityid = models.IntegerField(db_column='activityID')
#    producttypeid = models.ForeignKey(Type, db_column='materialTypeID')
#    quantity = models.IntegerField(db_column='quantity')
#    class Meta:
#        managed = False
#        db_table = 'industryActivityProducts'
#    def __str__(self):
#        return self.typeid.typename + " : " + self.materialtypeid.typename

@python_2_unicode_compatible
class Region(models.Model):
    regionid = models.AutoField(db_column='regionID', primary_key=True)
    regionname = models.CharField(db_column='regionName', max_length=200, blank=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    xmin = models.FloatField(db_column='xMin', blank=True, null=True)
    xmax = models.FloatField(db_column='xMax', blank=True, null=True)
    ymin = models.FloatField(db_column='yMin', blank=True, null=True)
    ymax = models.FloatField(db_column='yMax', blank=True, null=True)
    zmin = models.FloatField(db_column='zMin', blank=True, null=True)
    zmax = models.FloatField(db_column='zMax', blank=True, null=True)
    factionid = models.IntegerField(db_column='factionID', blank=True, null=True)
    radius = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mapRegions'
    def __str__(self):
        return self.regionname

@python_2_unicode_compatible
class Constellation(models.Model):
    regionid = models.ForeignKey(Region, db_column='regionID', blank=True, null=True)
    constellationid = models.AutoField(db_column='constellationID', primary_key=True)
    constellationname = models.CharField(db_column='constellationName', max_length=100, blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    xmin = models.FloatField(db_column='xMin', blank=True, null=True)
    xmax = models.FloatField(db_column='xMax', blank=True, null=True)
    ymin = models.FloatField(db_column='yMin', blank=True, null=True)
    ymax = models.FloatField(db_column='yMax', blank=True, null=True)
    zmin = models.FloatField(db_column='zMin', blank=True, null=True)
    zmax = models.FloatField(db_column='zMax', blank=True, null=True)
    factionid = models.IntegerField(db_column='factionID', blank=True, null=True)
    radius = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mapRegions'

@python_2_unicode_compatible
class SolarSystem(models.Model):
    regionid = models.ForeignKey(Region, db_column='regionID', blank=True, null=True)
    constellationid = models.ForeignKey(Constellation, db_column='constellationID', blank=True, null=True)
    solarsystemid = models.AutoField(db_column='solarSystemID', primary_key=True)
    solarsystemname = models.CharField(db_column='solarSystemName', max_length=100, blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    xmin = models.FloatField(db_column='xMin', blank=True, null=True)
    xmax = models.FloatField(db_column='xMax', blank=True, null=True)
    ymin = models.FloatField(db_column='yMin', blank=True, null=True)
    ymax = models.FloatField(db_column='yMax', blank=True, null=True)
    zmin = models.FloatField(db_column='zMin', blank=True, null=True)
    zmax = models.FloatField(db_column='zMax', blank=True, null=True)
    luminosity = models.FloatField(blank=True, null=True)
    border = models.BigIntegerField(blank=True, null=True)
    fringe = models.BigIntegerField(blank=True, null=True)
    corridor = models.BigIntegerField(blank=True, null=True)
    hub = models.BigIntegerField(blank=True, null=True)
    international = models.BigIntegerField(blank=True, null=True)
    regional = models.BigIntegerField(blank=True, null=True)
    constellation = models.BigIntegerField(blank=True, null=True)
    security = models.FloatField(blank=True, null=True)
    factionid = models.IntegerField(db_column='factionID', blank=True, null=True)
    radius = models.FloatField(blank=True, null=True)
    suntypeid = models.IntegerField(db_column='sunTypeID', blank=True, null=True)
    securityclass = models.CharField(db_column='securityClass', max_length=2, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mapSolarSystems'
    def __str__(self):
        return self.solarsystemname

@python_2_unicode_compatible
class Station(models.Model):
    stationid = models.IntegerField(db_column='stationID', primary_key=True)
    security = models.SmallIntegerField(blank=True, null=True)
    dockingcostpervolume = models.FloatField(db_column='dockingCostPerVolume', blank=True, null=True)
    maxshipvolumedockable = models.FloatField(db_column='maxShipVolumeDockable', blank=True, null=True)
    officerentalcost = models.IntegerField(db_column='officeRentalCost', blank=True, null=True)
    operationid = models.IntegerField(db_column='operationID', blank=True, null=True)
    stationtypeid = models.IntegerField(db_column='stationTypeID', blank=True, null=True)
    corporationid = models.IntegerField(db_column='corporationID', blank=True, null=True)
    solarsystemid = models.IntegerField(db_column='solarSystemID', blank=True, null=True)
    constellationid = models.IntegerField(db_column='constellationID', blank=True, null=True)
    regionid = models.IntegerField(db_column='regionID', blank=True, null=True)
    stationname = models.CharField(db_column='stationName', max_length=100, blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    reprocessingefficiency = models.FloatField(db_column='reprocessingEfficiency', blank=True, null=True)
    reprocessingstationstake = models.FloatField(db_column='reprocessingStationsTake', blank=True, null=True)
    reprocessinghangarflag = models.IntegerField(db_column='reprocessingHangarFlag', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'staStations'
    def __str__(self):
        return self.stationname
    def short(self):
        if not self.stationname:
            return None
        station_split = self.stationname.split(" - ", 2)
        station_abbr = ""
        for word in station_split[-1].split(" "):
            station_abbr += word[0]
        if len(station_split) > 2:
            return station_split[0] + ' / M' + station_split[1].split(" ")[1] + ' / ' + station_abbr

@python_2_unicode_compatible
class MarketOrder(models.Model):
    orderid = models.BigIntegerField(db_column='orderID', primary_key=True)
    generationdate = models.DateTimeField(db_column='generationDate')
    issuedate = models.DateTimeField(db_column='issueDate')
    typeid = models.ForeignKey(Type, db_column='typeID', db_constraint=False)
    price = models.FloatField()
    volentered = models.IntegerField(db_column='volEntered')
    volremaining = models.IntegerField(db_column='volRemaining')
    range = models.IntegerField()
    duration = models.IntegerField()
    minvolume = models.IntegerField(db_column='minVolume')
    bid = models.BooleanField()
    stationid = models.ForeignKey(Station, db_column='stationID', db_constraint=False)
    solarsystemid = models.ForeignKey(SolarSystem, db_column='solarSystemID')
    regionid = models.ForeignKey(Region, db_column='regionID')
    class Meta:
        db_table = 'marketOrders'
    def __str__(self):
        return str(self.typeid)

@python_2_unicode_compatible
class MarketHistory(models.Model):
    region = models.ForeignKey(Region, db_column='regionID')
    date = models.DateField()
    typeID = models.ForeignKey(Type, db_column='typeID', db_constraint=False)
    price_low = models.FloatField()
    price_high = models.FloatField()
    price_average = models.FloatField()
    quantity = models.BigIntegerField()
    num_orders = models.BigIntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = 'marketHistory'
    def __str__(self):
        return str(self.type)
