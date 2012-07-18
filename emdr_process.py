#!/usr/bin/env python2

from emds.formats import unified
from emds.common_utils import now_dtime_in_utc
import zlib
#import datetime
#import dateutil.parser
#import pytz
#import ujson as json
from hotqueue import HotQueue
import PySQLPool as pysqlpool
import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
import emdr_config as config
import cProfile

# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 10

# use a greenlet pool to cap the number of workers at a reasonable level
gpool = Pool(size=MAX_NUM_POOL_WORKERS)

queue = HotQueue("emdr", unix_socket_path="/tmp/redis.sock")
connection = pysqlpool.getNewConnection(username=config.dbuser, password=config.dbpass, host=config.dbhost, db=config.dbname)

def main():
  counter = 0
  for message in queue.consume():
    # gpool.spawn(process, message)
    counter += 1
    if counter > 200: 
      break
    else:
      gpool.spawn(process, message)

  # for i in range(50):
  #   gpool.spawn(process, queue.get(block=True)).join()
  

def process(message):
  query = pysqlpool.getNewQuery(connection)
  
  market_json = zlib.decompress(message)
  market_data = unified.parse_from_json(market_json)
  insertData = []
  deleteData = []
  
  if market_data.list_type == 'orders':
    orderIDs = []
    typeIDs = []
    if len(market_data) == 0:
      pass #TODO: Add support for empty orders
    else:
      for region in market_data.get_all_order_groups():
        # print("descending into region id %d" % region.region_id)
        for order in region: #TODO: Add timezone support
          insertData.append((order.order_id, str(order.generated_at).split("+", 1)[0], str(order.order_issue_date).split("+", 1)[0], order.type_id, round(order.price, 2), order.volume_entered, order.volume_remaining, order.order_range, order.order_duration, order.minimum_volume, int(order.is_bid), order.station_id, order.solar_system_id, order.region_id))
          orderIDs.append(str(int(order.order_id))) #hacky SQLi protection
          typeIDs.append(str(int(order.type_id)))
        deleteData.append((region.region_id,))
        sql = "DELETE FROM `marketOrders` WHERE `regionID` = %s AND `typeID` IN (" + ", ".join(list(set(typeIDs))) + ") AND `orderID` NOT IN (" + ", ".join(orderIDs) + ")"
        query.executeMany(sql, deleteData)
    sql  = 'INSERT INTO `marketOrders` (`orderID`, `generationDate`, `issueDate`, `typeID`, `price`, `volEntered`, '
    sql += '`volRemaining`, `range`, `duration`, `minVolume`, `bid`, `stationID`, `solarSystemID`, `regionID`) '
    sql += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
    sql += 'ON DUPLICATE KEY UPDATE '
    sql += '`issueDate`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`issueDate`), `issueDate`), '
    sql += '`typeID`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`typeID`), `typeID`), '
    sql += '`price`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`price`), `price`), '
    sql += '`volEntered`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`volEntered`), `volEntered`), '
    sql += '`volRemaining`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`volRemaining`), `volRemaining`), '
    sql += '`range`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`range`), `range`), '
    sql += '`duration`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`duration`), `duration`), '
    sql += '`minVolume`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`minVolume`), `minVolume`), '
    sql += '`bid`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`bid`), `bid`), '
    sql += '`stationID`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`stationID`), `stationID`), '
    sql += '`solarSystemID`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`solarSystemID`), `solarSystemID`), '
    sql += '`regionID`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`regionID`), `regionID`), '
    sql += '`generationDate`=IF(`generationDate` < VALUES(`generationDate`), VALUES(`generationDate`), `generationDate`)'
    query.executeMany(sql, insertData)
    print("Finished a job of %d market orders" % len(market_data))
  
  elif market_data.list_type == 'history': #TODO: Add support for history data
    print( "Received a batch of %d history entries" % len(market_data))
  
  gevent.sleep()
  pysqlpool.getNewPool().Commit()

if __name__ == '__main__':
  # main()
  cProfile.run("main()")
  # import sys
  # sys.sleep(5)
