#!/usr/bin/env python2

import sys
from emds.formats import unified
from emds.common_utils import now_dtime_in_utc
import zlib
from hotqueue import HotQueue
import PySQLPool as pysqlpool
import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
import emdr_config as config

# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 15

# use a greenlet pool to cap the number of workers at a reasonable level
gpool = Pool(size=MAX_NUM_POOL_WORKERS)

queue = HotQueue("emdr", unix_socket_path="/var/run/redis/redis.sock")
queue_history = HotQueue("emdr_history", unix_socket_path="/var/run/redis/redis.sock")
connection = pysqlpool.getNewConnection(username=config.dbuser, password=config.dbpass, unix_socket=config.dbsocket, db=config.dbname)
# connection = pysqlpool.getNewConnection(username=config.dbuser, password=config.dbpass, host=config.dbhost , db=config.dbname)

def main():
  for message in queue.consume():
    gpool.spawn(process, message)

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
      pass
    else:
      stuff = {}
      for region in market_data.get_all_order_groups():
        for order in region:
          # Timezone is silently discarded since it doesn't seem to be used in any messages I've seen
          insertData.append((order.order_id, str(order.generated_at).split("+", 1)[0], str(order.order_issue_date).split("+", 1)[0], order.type_id, round(order.price, 2), order.volume_entered, order.volume_remaining, order.order_range, order.order_duration, order.minimum_volume, int(order.is_bid), order.station_id, order.solar_system_id, order.region_id))
          orderIDs.append(str(int(order.order_id)))  # hacky SQLi protection
          typeIDs.append(str(int(order.type_id)))
        deleteData.append((region.region_id,))
        sql = "DELETE FROM `marketOrdersMem` WHERE `regionID` = %s AND `typeID` IN (" + ", ".join(list(set(typeIDs))) + ") AND `orderID` NOT IN (" + ", ".join(orderIDs) + ")"
        query.executeMany(sql, deleteData)

    # This query uses INSERT ... ON DUPLICATE KEY UPDATE syntax. It has a condition to only update the row if the new row's generationDate is newer than the stored generationDate. We don't want to replace our data with older data. We don't use REPLACE because we need to have this condition. Querying the table for existing data is possible for a cleaner statement, but it would probably result in slower inserts.
    sql  = 'INSERT INTO `marketOrdersMem` (`orderID`, `generationDate`, `issueDate`, `typeID`, `price`, `volEntered`, '
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
    # print("Finished a job of %d market orders" % len(market_data))
  
  elif market_data.list_type == 'history':
    queue_history.put(market_data)
    #pass
    # insertData = []
    # for history in market_data.get_all_entries_ungrouped():
    #   insertData.append((history.type_id, history.region_id, history.historical_date, history.low_price, history.high_price, history.average_price, history.total_quantity, history.num_orders, history.generated_at))

    # sql  = 'INSERT INTO `items_history` (`type_id`, `region_id`, `date`, `price_low`, `price_high`, `price_average`, '
    # sql += '`quantity`, `num_orders`, `created`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) '
    # sql += 'ON DUPLICATE KEY UPDATE '
    # sql += '`price_low`=VALUES(`price_low`), `price_high`=VALUES(`price_high`), `price_average`=VALUES(`price_average`), '
    # sql += '`quantity`=VALUES(`quantity`), `num_orders`=VALUES(`num_orders`)'
    # query.executeMany(sql, insertData)

  gevent.sleep()
  pysqlpool.getNewPool().Commit()
  sys.stdout.write(".")
  sys.stdout.flush()

if __name__ == '__main__':
  main()
  # cProfile.run("main()")
