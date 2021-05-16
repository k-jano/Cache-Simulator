import json
import time
from datetime import datetime
from threading import Thread

import redis

from node import Node

channel = 'SIMULATOR'

class Simulator():
  def __init__(self):
    self.wf_key = 1
    self.keys_in = []
    self.keys_out = []
    self.r = redis.StrictRedis(host="localhost", port=6379, db=0)
    self.nodes = [Node(0), Node(1), Node(2)]
    self.p = self.r.pubsub()

  def bytes_to_string(self, byte_obj):
    return byte_obj.decode("utf-8")

  def sort_keys(self):
    self.keys_in.sort()
    self.keys_out.sort()

  def get_workflow(self):
    for key in self.r.scan_iter("wf:" + str(self.wf_key) + ":task:[0-9]*:*"):
      key_str = self.bytes_to_string(key)
      # print(key_str)
      self.keys_in.append(key) if key_str.endswith('ins') else self.keys_out.append(key)
    
    # for key in self.keys_in:
    #   print(self.r.zrange(key, 0, -1))

    self.sort_keys()

  def get_most_accurate_node(self):
    best_node = None
    for node in self.nodes:
      if not best_node:
        best_node = node
      else:
        if node.get_avalaible_vcpu() > best_node.get_avalaible_vcpu():
          best_node = node

    return best_node

  def schedule(self, job_id):
    node = self.get_most_accurate_node()
    print('[%s] Job %s scheduled on node %s' % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), job_id, node.id))
    node.execute(job_id)

  def thread_routine(self, msg):
    data = self.bytes_to_string(msg.get('data'))
    self.schedule(data)
    self.r.publish(data, 'Processed')

  def routine(self, msg):
    print(msg)
    if msg.get('type') != 'subscribe':
      #TODO Schedule and mock execution
      thread = Thread(target = self.thread_routine, args=(msg, ))
      thread.start()

  def subscribe(self):
    try:
      self.p.subscribe(**{channel:self.routine})
      t = self.p.run_in_thread(sleep_time = 0.001)
      while True:
        pass
    except KeyboardInterrupt:
      print('Keyboard Interrupt')
      t.stop()

if __name__ == "__main__":
  simulator = Simulator()
  simulator.subscribe()
