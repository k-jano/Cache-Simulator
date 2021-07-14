import json
import time
from datetime import datetime
from threading import Thread
import yaml
from collections import deque

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
    #self.nodes = [Node(0, self.BeladyFreq), Node(1, self.BeladyFreq), Node(2, self.BeladyFreq)]
    self.p = self.r.pubsub()
    self.flag = True
    self.prepare_nodes()
    self.queue = deque([])
    self.thread_sleep_interval = 0.001
    self.cache_factor = config['simulator']['cache_factor']
    self.load_data()

  def load_data(self):
    with open('data.json') as json_file:
      data = json.load(json_file)
      self.data = data

  def prepare_nodes(self):
    nodes = []
    for i in range(config['simulator']['nodes']):
      nodes.append(Node(i, self.BeladyFreq))

    self.nodes = nodes

  def bytes_to_string(self, byte_obj):
    return byte_obj.decode("utf-8")

  def filter_nodes(self, job_id):
    job_nr = job_id.split(":")[2]
    available_nodes = []
    for node in self.nodes:
      if node.get_avalaible_cpu() > self.data[job_nr]['cpu']:
        available_nodes.append(node)

    return available_nodes

  def get_best_score_node(self, available_nodes, ins):
    ins_list = []
    for file in ins:
      if file == "length":
        break
      ins_list.append(file)
    
    if not available_nodes:
      return None
    
    best_node = None
    scores = [0] * len(available_nodes)
    for i in range(len(available_nodes)):
      scores[i] = (1 - self.cache_factor) * available_nodes[i].get_avalaible_cpu() / (config['simulator']['vcpu'] * 100) 
      + self.cache_factor * available_nodes[i].calucate_cache_score(ins_list)

    return available_nodes[scores.index(max(scores))]

  def scheduler_routine(self, job_id, data, node):
    node.execute(job_id, data)

    self.r.publish(job_id, 'Processed')

    if job_id.split(":")[2] == config['simulator']['last_id']:
      self.print_output()

  def schedule(self):
    while True:
      if self.queue:
        job = self.queue.popleft()
        job_id = job['key']
        data = job['data']

        available_nodes = self.filter_nodes(job_id)
        node = self.get_best_score_node(available_nodes, data.get("ins"))
        #node = self.get_most_accurate_node()
        if node == None:
          self.queue.appendleft(job)
        else:
          print('[%s] Job %s scheduled on node %s' % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), job_id, node.id))
          t = Thread(target = self.scheduler_routine, daemon=True, args=(job_id, data, node))
          t.start()
      else:
        time.sleep(self.thread_sleep_interval)

  def print_output(self):
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

  def thread_routine(self, msg):
    data = json.loads(self.bytes_to_string(msg.get('data')))
    key = data.get('key')
    # if key.split(":")[2] == "619":
    #   print(json.dumps(data, indent=4))
    
    self.queue.append({
      'key': key,
      'data': data
    })
    #self.schedule(key, data)
    #self.r.publish(key, 'Processed')

  def routine(self, msg):
    if msg.get('type') != 'subscribe':
      #TODO Schedule and mock execution
      thread = Thread(target = self.thread_routine, args=(msg, ))
      thread.start()

  def subscribe(self):
    try:
      self.p.subscribe(**{config['redis']['channel']:self.routine})
      t = self.p.run_in_thread(sleep_time = self.thread_sleep_interval)
      scheduler = Thread(target = self.schedule, daemon=True)
      scheduler.start()
      while True:
        pass
    except KeyboardInterrupt:
      print('Keyboard Interrupt')
      t.stop()

if __name__ == "__main__":
  simulator = Simulator()
  simulator.subscribe()
