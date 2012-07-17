#!/usr/bin/env python2
"""
Get the data from EMDR and shove it into the database
Greg Oberfield gregoberfield@gmail.com
"""

from emds.formats import unified
from emds.common_utils import now_dtime_in_utc
import zlib
#import datetime
#import dateutil.parser
#import pytz
#import sys
#import ujson as json
# Need ast to convert from string to dictionary
#import ast
from hotqueue import HotQueue
import PySQLPool as pysqlpool
import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
import emdr_config as config

# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 200

# use a greenlet pool to cap the number of workers at a reasonable level
gpool = Pool(size=MAX_NUM_POOL_WORKERS)

queue = HotQueue("emdr", unix_socket_path="/tmp/redis.sock")
connection = pysqlpool.getNewConnection(username=config.dbuser, password=config.dbpass, host=config.dbhost, db=config.dbname)

def main():
  # for message in queue.consume():
  #   gpool.spawn(thread, message)

  gpool.spawn(thread, queue.get(block=True)).join()
  

def thread(message):
  query = pysqlpool.getNewQuery(connection)
  
  market_json = zlib.decompress(message)
  market_data = unified.parse_from_json(market_json)
  insertData = []
  deleteData = []

  if market_data.list_type == 'orders':
    orderIDs = []
    if len(market_data) == 0:
      pass #TODO: Add support for empty orders
    else:
      for region in market_data.get_all_order_groups():
        # print("descending into region id %d" % region.region_id)
        for order in region: #TODO: Add timezone support
          insertData.append((order.order_id, str(order.generated_at).split("+", 1)[0], str(order.order_issue_date).split("+", 1)[0], order.type_id, round(order.price, 2), order.volume_entered, order.volume_remaining, order.order_range, order.order_duration, order.minimum_volume, int(order.is_bid), order.station_id, order.solar_system_id, order.region_id))
          orderIDs.append(str(int(order.order_id))) #hacky SQLi protection
        deleteData.append((0,))
        sql = "DELETE FROM `marketOrders` WHERE `regionID` = %s AND `orderID` NOT IN (" + ", ".join(orderIDs) + ")"
        query.executeMany(sql, deleteData)
        # print(sql)
    sql =  "INSERT INTO `marketOrders` (`orderID`, `generationDate`, `issueDate`, `typeID`, `price`, `volEntered`, `volRemaining`, `range`, `duration`, `minVolume`, `bid`, `stationID`, `solarSystemID`, `regionID`) "
    sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
    sql += "ON DUPLICATE KEY UPDATE `generationDate`=VALUES(`generationDate`), `issueDate`=VALUES(`issueDate`), `typeID`=VALUES(`typeID`), `price`=VALUES(`price`), `volEntered`=VALUES(`volEntered`), `volRemaining`=VALUES(`volRemaining`), `range`=VALUES(`range`), `duration`=VALUES(`duration`), `minVolume`=VALUES(`minVolume`), `bid`=VALUES(`bid`), `stationID`=VALUES(`stationID`), `solarSystemID`=VALUES(`solarSystemID`), `regionID`=VALUES(`regionID`)"
    query.executeMany(sql, insertData)
    # print(sql)


  elif market_data.list_type == 'history': #TODO: Add support for history data
    print( "Received a batch of %d history entries" % len(market_data))
  
  # gevent.sleep()
  pysqlpool.getNewPool().Commit()

if __name__ == '__main__':
  main()
