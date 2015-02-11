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
MAX_NUM_POOL_WORKERS = 3

# use a greenlet pool to cap the number of workers at a reasonable level
gpool = Pool(size=MAX_NUM_POOL_WORKERS)

queue_history = HotQueue("emdr_history", unix_socket_path="/var/run/redis/redis.sock")
connection = pysqlpool.getNewConnection(username=config.dbuser, password=config.dbpass, unix_socket=config.dbsocket, db=config.dbname)
# connection = pysqlpool.getNewConnection(username=config.dbuser, password=config.dbpass, host=config.dbhost , db=config.dbname)

def main():
  for message in queue_history.consume():
    gpool.spawn(process, message)

def process(market_data):
  query = pysqlpool.getNewQuery(connection)

  insertData = []
  for history in market_data.get_all_entries_ungrouped():
    insertData.append((history.type_id, history.region_id, history.historical_date, history.low_price, history.high_price, history.average_price, history.total_quantity, history.num_orders, history.generated_at))

  sql  = 'INSERT INTO `items_history` (`type_id`, `region_id`, `date`, `price_low`, `price_high`, `price_average`, '
  sql += '`quantity`, `num_orders`, `created`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) '
  sql += 'ON DUPLICATE KEY UPDATE '
  sql += '`price_low`=VALUES(`price_low`), `price_high`=VALUES(`price_high`), `price_average`=VALUES(`price_average`), '
  sql += '`quantity`=VALUES(`quantity`), `num_orders`=VALUES(`num_orders`)'
  query.executeMany(sql, insertData)

  gevent.sleep()
  pysqlpool.getNewPool().Commit()
  sys.stdout.write(".")
  sys.stdout.flush()

if __name__ == '__main__':
  main()
  # cProfile.run("main()")
