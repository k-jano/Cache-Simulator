import time
import json

from algorithms.FIFO import FIFO
from algorithms.LFU import LFU
from algorithms.LRU import LRU
from algorithms.RR import RR
from algorithms.Belady import Belady

class Node():
  def __init__(self, id, BeladyFreq):
    self.cache = []
    self.cpu = 100
    self.id = id
    self.data = None
    self.policies = []
    self.file_size = None
    self.BeladyFreq = BeladyFreq

    self.load_data()

  def load_data(self):
    with open('data.json') as json_file:
      data = json.load(json_file)
      self.data = data

    with open('file_size.json') as json_file:
      file_size = json.load(json_file)
      self.file_size = file_size

    cache_size = 1000 * 1024 * 1024
    self.policies = [FIFO(cache_size, self.file_size),
      LFU(cache_size, self.file_size),
      LRU(cache_size, self.file_size),
      RR(cache_size, self.file_size), 
      Belady(cache_size, self.file_size, self.BeladyFreq)]

  def get_avalaible_cpu(self):
    return self.cpu

  def mock_execute(self):
    print('Start mocking exectuion %d' % self.env.now)
    yield self.env.timeout(5000)
    print('End mocking exectuion %d' % self.env.now)

  def get_swap(self):
    swap_count_list = []
    for policy in self.policies:
      swap_count_list.append(policy.get_swap_count())
    return swap_count_list

  def get_hit(self):
    hit_count_list = []
    for policy in self.policies:
      hit_count_list.append(policy.get_hit_count())
    return hit_count_list

  def get_miss(self):
    miss_count_list = []
    for policy in self.policies:
      miss_count_list.append(policy.get_miss_count())
    return miss_count_list

  def execute(self, job_id, msg):
    job = job_id.split(":")
    sleep_time = self.data[str(job[2])]["time"]
    self.cpu -= self.data[str(job[2])]["cpu"]

    for file in msg.get("ins"):
      if file == "length":
        break
      for policy in self.policies:
        policy.process(msg.get("ins").get(file).get("name"))

    time.sleep(sleep_time)

    for file in msg.get("outs"):
      if file == "length":
        break
      for policy in self.policies:
        policy.process(msg.get("outs").get(file).get("name"))

    self.cpu += self.data[str(job[2])]["cpu"]
      #self.memory += self.data[str(job[2])]["cpu"]
