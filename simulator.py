import json
import time
from datetime import datetime
from threading import Thread
import yaml

import redis

from node import Node
from helpers.belady_freq import BeladyFreq

config = yaml.safe_load(open("./config.yml"))

class Simulator():
  def __init__(self):
    self.wf_key = 1
    self.keys_in = []
    self.keys_out = []
    self.r = redis.StrictRedis(host=config['redis']['address'], port=config['redis']['port'], db=0)
    self.BeladyFreq = BeladyFreq()
    self.nodes = [Node(0, self.BeladyFreq), Node(1, self.BeladyFreq), Node(2, self.BeladyFreq)]
    self.p = self.r.pubsub()
    self.flag = True

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
        if node.get_avalaible_cpu() > best_node.get_avalaible_cpu():
          best_node = node

    return best_node

  def schedule(self, job_id, msg):
    node = self.get_most_accurate_node()
    print('[%s] Job %s scheduled on node %s' % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), job_id, node.id))
    node.execute(job_id, msg)

  def thread_routine(self, msg):
    data = json.loads(self.bytes_to_string(msg.get('data')))
    key = data.get('key')
    # if key.split(":")[2] == "619":
    #   print(json.dumps(data, indent=4))
    self.schedule(key, data)
    self.r.publish(key, 'Processed')
    if key.split(":")[2] == config['simulator']['last_id']:
      print('--- HIT ---')
      hit_count = [0, 0, 0, 0, 0]
      for node in self.nodes:
        hit_count = [x+y for x, y in zip(hit_count, node.get_hit())]
        #print(node.get_hit())
      print("Total hit_count " + str(hit_count))

      print('--- MISS ---')
      miss_count = [0, 0, 0, 0, 0]
      for node in self.nodes:
        miss_count = [x+y for x, y in zip(miss_count, node.get_miss())]
        #print(node.get_miss())
      print("Total miss_count " + str(miss_count))

      print('--- SWAP ---')
      swap_count = [0, 0, 0, 0, 0]
      for node in self.nodes:
        swap_count = [x+y for x, y in zip(swap_count, node.get_swap())]
        #print(node.get_swap())
      print("Total swap_count " + str(swap_count))

  def routine(self, msg):
    if msg.get('type') != 'subscribe':
      #TODO Schedule and mock execution
      thread = Thread(target = self.thread_routine, args=(msg, ))
      thread.start()

  def subscribe(self):
    try:
      self.p.subscribe(**{config['redis']['channel']:self.routine})
      t = self.p.run_in_thread(sleep_time = 0.001)
      while True:
        pass
    except KeyboardInterrupt:
      print('Keyboard Interrupt')
      t.stop()

if __name__ == "__main__":
  simulator = Simulator()
  simulator.subscribe()
