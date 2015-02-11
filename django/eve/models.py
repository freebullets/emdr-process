# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

# class Invblueprinttypes(models.Model):
#     blueprinttypeid = models.IntegerField(db_column='blueprintTypeID', primary_key=True) # Field name made lowercase.
#     parentblueprinttypeid = models.IntegerField(db_column='parentBlueprintTypeID', blank=True, null=True) # Field name made lowercase.
#     producttypeid = models.IntegerField(db_column='productTypeID', blank=True, null=True) # Field name made lowercase.
#     productiontime = models.IntegerField(db_column='productionTime', blank=True, null=True) # Field name made lowercase.
#     techlevel = models.IntegerField(db_column='techLevel', blank=True, null=True) # Field name made lowercase.
#     researchproductivitytime = models.IntegerField(db_column='researchProductivityTime', blank=True, null=True) # Field name made lowercase.
#     researchmaterialtime = models.IntegerField(db_column='researchMaterialTime', blank=True, null=True) # Field name made lowercase.
#     researchcopytime = models.IntegerField(db_column='researchCopyTime', blank=True, null=True) # Field name made lowercase.
#     researchtechtime = models.IntegerField(db_column='researchTechTime', blank=True, null=True) # Field name made lowercase.
#     productivitymodifier = models.IntegerField(db_column='productivityModifier', blank=True, null=True) # Field name made lowercase.
#     materialmodifier = models.IntegerField(db_column='materialModifier', blank=True, null=True) # Field name made lowercase.
#     wastefactor = models.IntegerField(db_column='wasteFactor', blank=True, null=True) # Field name made lowercase.
#     maxproductionlimit = models.IntegerField(db_column='maxProductionLimit', blank=True, null=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'invBlueprintTypes'

class MarketGroup(models.Model):
    marketgroupid = models.IntegerField(db_column='marketGroupID', primary_key=True) # Field name made lowercase.
    parentgroupid = models.IntegerField(db_column='parentGroupID', blank=True, null=True) # Field name made lowercase.
    marketgroupname = models.CharField(db_column='marketGroupName', max_length=200, blank=True) # Field name made lowercase.
    description = models.CharField(max_length=6000, blank=True)
    iconid = models.IntegerField(db_column='iconID', blank=True, null=True) # Field name made lowercase.
    hastypes = models.IntegerField(db_column='hasTypes', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'invMarketGroups'
    def __unicode__(self):
        return self.marketgroupname

# class Invmetagroups(models.Model):
#     metagroupid = models.IntegerField(db_column='metaGroupID', primary_key=True) # Field name made lowercase.
#     metagroupname = models.CharField(db_column='metaGroupName', max_length=200, blank=True) # Field name made lowercase.
#     description = models.CharField(max_length=2000, blank=True)
#     iconid = models.IntegerField(db_column='iconID', blank=True, null=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'invMetaGroups'

# class Invmetatypes(models.Model):
#     typeid = models.IntegerField(db_column='typeID', primary_key=True) # Field name made lowercase.
#     parenttypeid = models.IntegerField(db_column='parentTypeID', blank=True, null=True) # Field name made lowercase.
#     metagroupid = models.IntegerField(db_column='metaGroupID', blank=True, null=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'invMetaTypes'

class Type(models.Model):
    typeid = models.IntegerField(db_column='typeID', primary_key=True) # Field name made lowercase.
    groupid = models.IntegerField(db_column='groupID', blank=True, null=True) # Field name made lowercase.
    typename = models.CharField(db_column='typeName', max_length=200, blank=True) # Field name made lowercase.
    description = models.CharField(max_length=6000, blank=True)
    mass = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    portionsize = models.IntegerField(db_column='portionSize', blank=True, null=True) # Field name made lowercase.
    raceid = models.IntegerField(db_column='raceID', blank=True, null=True) # Field name made lowercase.
    baseprice = models.DecimalField(db_column='basePrice', max_digits=19, decimal_places=4, blank=True, null=True) # Field name made lowercase.
    published = models.IntegerField(blank=True, null=True)
    marketgroupid = models.ForeignKey(MarketGroup, db_column='marketGroupID', blank=True, null=True) # Field name made lowercase.
    chanceofduplicating = models.FloatField(db_column='chanceOfDuplicating', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'invTypes'
    def __unicode__(self):
        return self.typename

class Region(models.Model):
    regionid = models.IntegerField(db_column='regionID', primary_key=True) # Field name made lowercase.
    regionname = models.CharField(db_column='regionName', max_length=200, blank=True) # Field name made lowercase.
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    xmin = models.FloatField(db_column='xMin', blank=True, null=True) # Field name made lowercase.
    xmax = models.FloatField(db_column='xMax', blank=True, null=True) # Field name made lowercase.
    ymin = models.FloatField(db_column='yMin', blank=True, null=True) # Field name made lowercase.
    ymax = models.FloatField(db_column='yMax', blank=True, null=True) # Field name made lowercase.
    zmin = models.FloatField(db_column='zMin', blank=True, null=True) # Field name made lowercase.
    zmax = models.FloatField(db_column='zMax', blank=True, null=True) # Field name made lowercase.
    factionid = models.IntegerField(db_column='factionID', blank=True, null=True) # Field name made lowercase.
    radius = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mapRegions'
    def __unicode__(self):
        return self.regionname

class SolarSystem(models.Model):
    regionid = models.IntegerField(db_column='regionID', blank=True, null=True) # Field name made lowercase.
    constellationid = models.IntegerField(db_column='constellationID', blank=True, null=True) # Field name made lowercase.
    solarsystemid = models.IntegerField(db_column='solarSystemID', primary_key=True) # Field name made lowercase.
    solarsystemname = models.CharField(db_column='solarSystemName', max_length=200, blank=True) # Field name made lowercase.
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    xmin = models.FloatField(db_column='xMin', blank=True, null=True) # Field name made lowercase.
    xmax = models.FloatField(db_column='xMax', blank=True, null=True) # Field name made lowercase.
    ymin = models.FloatField(db_column='yMin', blank=True, null=True) # Field name made lowercase.
    ymax = models.FloatField(db_column='yMax', blank=True, null=True) # Field name made lowercase.
    zmin = models.FloatField(db_column='zMin', blank=True, null=True) # Field name made lowercase.
    zmax = models.FloatField(db_column='zMax', blank=True, null=True) # Field name made lowercase.
    luminosity = models.FloatField(blank=True, null=True)
    border = models.IntegerField(blank=True, null=True)
    fringe = models.IntegerField(blank=True, null=True)
    corridor = models.IntegerField(blank=True, null=True)
    hub = models.IntegerField(blank=True, null=True)
    international = models.IntegerField(blank=True, null=True)
    regional = models.IntegerField(blank=True, null=True)
    constellation = models.IntegerField(blank=True, null=True)
    security = models.FloatField(blank=True, null=True)
    factionid = models.IntegerField(db_column='factionID', blank=True, null=True) # Field name made lowercase.
    radius = models.FloatField(blank=True, null=True)
    suntypeid = models.IntegerField(db_column='sunTypeID', blank=True, null=True) # Field name made lowercase.
    securityclass = models.CharField(db_column='securityClass', max_length=2, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'mapSolarSystems'
    def __unicode__(self):
        return self.solarsystemname

class Station(models.Model):
    stationid = models.IntegerField(db_column='stationID', primary_key=True) # Field name made lowercase.
    security = models.IntegerField(blank=True, null=True)
    dockingcostpervolume = models.FloatField(db_column='dockingCostPerVolume', blank=True, null=True) # Field name made lowercase.
    maxshipvolumedockable = models.FloatField(db_column='maxShipVolumeDockable', blank=True, null=True) # Field name made lowercase.
    officerentalcost = models.IntegerField(db_column='officeRentalCost', blank=True, null=True) # Field name made lowercase.
    operationid = models.IntegerField(db_column='operationID', blank=True, null=True) # Field name made lowercase.
    stationtypeid = models.IntegerField(db_column='stationTypeID', blank=True, null=True) # Field name made lowercase.
    corporationid = models.IntegerField(db_column='corporationID', blank=True, null=True) # Field name made lowercase.
    solarsystemid = models.IntegerField(db_column='solarSystemID', blank=True, null=True) # Field name made lowercase.
    constellationid = models.IntegerField(db_column='constellationID', blank=True, null=True) # Field name made lowercase.
    regionid = models.IntegerField(db_column='regionID', blank=True, null=True) # Field name made lowercase.
    stationname = models.CharField(db_column='stationName', max_length=200, blank=True) # Field name made lowercase.
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    reprocessingefficiency = models.FloatField(db_column='reprocessingEfficiency', blank=True, null=True) # Field name made lowercase.
    reprocessingstationstake = models.FloatField(db_column='reprocessingStationsTake', blank=True, null=True) # Field name made lowercase.
    reprocessinghangarflag = models.IntegerField(db_column='reprocessingHangarFlag', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'staStations'
    def __unicode__(self):
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

class MarketOrder(models.Model):
    orderid = models.BigIntegerField(db_column='orderID', primary_key=True) # Field name made lowercase.
    generationdate = models.DateTimeField(db_column='generationDate') # Field name made lowercase.
    issuedate = models.DateTimeField(db_column='issueDate') # Field name made lowercase.
    typeid = models.ForeignKey(Type, db_column='typeID') # Field name made lowercase.
    price = models.FloatField()
    volentered = models.IntegerField(db_column='volEntered') # Field name made lowercase.
    volremaining = models.IntegerField(db_column='volRemaining') # Field name made lowercase.
    range = models.IntegerField()
    duration = models.IntegerField()
    minvolume = models.IntegerField(db_column='minVolume') # Field name made lowercase.
    bid = models.BooleanField()
    stationid = models.ForeignKey(Station, db_column='stationID') # Field name made lowercase.
    solarsystemid = models.ForeignKey(SolarSystem, db_column='solarSystemID') # Field name made lowercase.
    regionid = models.ForeignKey(Region, db_column='regionID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'marketOrders'
    def __unicode__(self):
        return unicode(self.typeid)

class MarketHistory(models.Model):
    region = models.ForeignKey(Region, db_column='region_id')
    date = models.DateField()
    type = models.ForeignKey(Type, db_column='type_id')
    price_low = models.FloatField()
    price_high = models.FloatField()
    price_average = models.FloatField()
    quantity = models.BigIntegerField()
    num_orders = models.BigIntegerField()
    created = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'items_history_new'
    def __unicode__(self):
        return unicode(self.type)

# class Ramactivities(models.Model):
#     activityid = models.IntegerField(db_column='activityID', primary_key=True) # Field name made lowercase.
#     activityname = models.CharField(db_column='activityName', max_length=200, blank=True) # Field name made lowercase.
#     iconno = models.CharField(db_column='iconNo', max_length=5, blank=True) # Field name made lowercase.
#     description = models.CharField(max_length=2000, blank=True)
#     published = models.IntegerField(blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'ramActivities'

# class Ramassemblylinestations(models.Model):
#     stationid = models.IntegerField(db_column='stationID') # Field name made lowercase.
#     assemblylinetypeid = models.IntegerField(db_column='assemblyLineTypeID') # Field name made lowercase.
#     quantity = models.IntegerField(blank=True, null=True)
#     stationtypeid = models.IntegerField(db_column='stationTypeID', blank=True, null=True) # Field name made lowercase.
#     ownerid = models.IntegerField(db_column='ownerID', blank=True, null=True) # Field name made lowercase.
#     solarsystemid = models.IntegerField(db_column='solarSystemID', blank=True, null=True) # Field name made lowercase.
#     regionid = models.IntegerField(db_column='regionID', blank=True, null=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'ramAssemblyLineStations'

# class Ramassemblylinetypedetailpercategory(models.Model):
#     assemblylinetypeid = models.IntegerField(db_column='assemblyLineTypeID') # Field name made lowercase.
#     categoryid = models.IntegerField(db_column='categoryID') # Field name made lowercase.
#     timemultiplier = models.FloatField(db_column='timeMultiplier', blank=True, null=True) # Field name made lowercase.
#     materialmultiplier = models.FloatField(db_column='materialMultiplier', blank=True, null=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'ramAssemblyLineTypeDetailPerCategory'

# class Ramassemblylinetypedetailpergroup(models.Model):
#     assemblylinetypeid = models.IntegerField(db_column='assemblyLineTypeID') # Field name made lowercase.
#     groupid = models.IntegerField(db_column='groupID') # Field name made lowercase.
#     timemultiplier = models.FloatField(db_column='timeMultiplier', blank=True, null=True) # Field name made lowercase.
#     materialmultiplier = models.FloatField(db_column='materialMultiplier', blank=True, null=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'ramAssemblyLineTypeDetailPerGroup'

# class Ramassemblylinetypes(models.Model):
#     assemblylinetypeid = models.IntegerField(db_column='assemblyLineTypeID', primary_key=True) # Field name made lowercase.
#     assemblylinetypename = models.CharField(db_column='assemblyLineTypeName', max_length=200, blank=True) # Field name made lowercase.
#     description = models.CharField(max_length=2000, blank=True)
#     basetimemultiplier = models.FloatField(db_column='baseTimeMultiplier', blank=True, null=True) # Field name made lowercase.
#     basematerialmultiplier = models.FloatField(db_column='baseMaterialMultiplier', blank=True, null=True) # Field name made lowercase.
#     volume = models.FloatField(blank=True, null=True)
#     activityid = models.IntegerField(db_column='activityID', blank=True, null=True) # Field name made lowercase.
#     mincostperhour = models.FloatField(db_column='minCostPerHour', blank=True, null=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'ramAssemblyLineTypes'

# class Ramassemblylines(models.Model):
#     assemblylineid = models.IntegerField(db_column='assemblyLineID', primary_key=True) # Field name made lowercase.
#     assemblylinetypeid = models.IntegerField(db_column='assemblyLineTypeID', blank=True, null=True) # Field name made lowercase.
#     containerid = models.IntegerField(db_column='containerID', blank=True, null=True) # Field name made lowercase.
#     nextfreetime = models.DateTimeField(db_column='nextFreeTime', blank=True, null=True) # Field name made lowercase.
#     uigroupingid = models.IntegerField(db_column='UIGroupingID', blank=True, null=True) # Field name made lowercase.
#     costinstall = models.FloatField(db_column='costInstall', blank=True, null=True) # Field name made lowercase.
#     costperhour = models.FloatField(db_column='costPerHour', blank=True, null=True) # Field name made lowercase.
#     restrictionmask = models.IntegerField(db_column='restrictionMask', blank=True, null=True) # Field name made lowercase.
#     discountpergoodstandingpoint = models.FloatField(db_column='discountPerGoodStandingPoint', blank=True, null=True) # Field name made lowercase.
#     surchargeperbadstandingpoint = models.FloatField(db_column='surchargePerBadStandingPoint', blank=True, null=True) # Field name made lowercase.
#     minimumstanding = models.FloatField(db_column='minimumStanding', blank=True, null=True) # Field name made lowercase.
#     minimumcharsecurity = models.FloatField(db_column='minimumCharSecurity', blank=True, null=True) # Field name made lowercase.
#     minimumcorpsecurity = models.FloatField(db_column='minimumCorpSecurity', blank=True, null=True) # Field name made lowercase.
#     maximumcharsecurity = models.FloatField(db_column='maximumCharSecurity', blank=True, null=True) # Field name made lowercase.
#     maximumcorpsecurity = models.FloatField(db_column='maximumCorpSecurity', blank=True, null=True) # Field name made lowercase.
#     ownerid = models.IntegerField(db_column='ownerID', blank=True, null=True) # Field name made lowercase.
#     activityid = models.IntegerField(db_column='activityID', blank=True, null=True) # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'ramAssemblyLines'

# class Raminstallationtypecontents(models.Model):
#     installationtypeid = models.IntegerField(db_column='installationTypeID') # Field name made lowercase.
#     assemblylinetypeid = models.IntegerField(db_column='assemblyLineTypeID') # Field name made lowercase.
#     quantity = models.IntegerField(blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'ramInstallationTypeContents'

# class Ramtyperequirements(models.Model):
#     typeid = models.IntegerField(db_column='typeID') # Field name made lowercase.
#     activityid = models.IntegerField(db_column='activityID') # Field name made lowercase.
#     requiredtypeid = models.IntegerField(db_column='requiredTypeID') # Field name made lowercase.
#     quantity = models.IntegerField(blank=True, null=True)
#     damageperjob = models.FloatField(db_column='damagePerJob', blank=True, null=True) # Field name made lowercase.
#     recycle = models.IntegerField(blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'ramTypeRequirements'
