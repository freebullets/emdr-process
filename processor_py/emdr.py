#!/usr/bin/env python2
"""
Get the data from EMDR and shove it into the redis queue
Greg Oberfield gregoberfield@gmail.com
"""

import sys
import zlib
import zmq.green as zmq
import gevent
from gevent.pool import Pool
from gevent import monkey; gevent.monkey.patch_all()
from hotqueue import HotQueue

# Max number of greenlet workers
MAX_NUM_POOL_WORKERS = 200

# Change this to point to whatever relay you want to use
receiver_uri = 'tcp://relay-us-central-1.eve-emdr.com:8050'
#receiver_uri = 'tcp://relay-us-east-1.eve-emdr.com:8050'

#receiver_uri = 'tcp://localhost:8050'
#receiver_uri = 'tcp://192.168.1.11:8050'

queue = HotQueue("emdr", unix_socket_path="/var/run/redis/redis.sock")

def main():
  """
  main flow of the app
  """
  
  context = zmq.Context()
  subscriber = context.socket(zmq.SUB)
  
  subscriber.connect(receiver_uri)
  # disable filtering
  subscriber.setsockopt(zmq.SUBSCRIBE, "")
  
  print("Connected to %s" % receiver_uri)
  
  # use a greenlet pool to cap the number of workers at a reasonable level
  greenlet_pool = Pool(size=MAX_NUM_POOL_WORKERS)
  
  print("Consumer daemon started, waiting for jobs...")
  
  while True:
    greenlet_pool.spawn(worker, subscriber.recv())
    
def worker(job_json):
  """
  For every incoming message, this worker function is called.  Be extremely
  careful not to do anything cpu intensive here, or you will see blocking.
  Sockets are async under gevent, so those are fair game
  """

  # Push the message onto the queue
  import random
  print random.random()
  queue.put(job_json)
  #sys.stdout.write(".")
  #sys.stdout.flush()
  
if __name__ == '__main__':
  main()
