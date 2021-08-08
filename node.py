import time
import json
import yaml

from algorithms.FIFO import FIFO
from algorithms.LFU import LFU
from algorithms.LRU import LRU
from algorithms.RR import RR
from algorithms.Belady import Belady
from helpers.mock_download import mock_download

config = yaml.safe_load(open("./config.yml"))

class Node():
  def __init__(self, id, BeladyFreq, downloader):
    self.cache = []
    self.cpu = config['simulator']['vcpu'] * 100
    self.id = id
    self.data = None
    self.policies = []
    self.file_size = None
    self.BeladyFreq = BeladyFreq
    self.downloader = downloader

    self.load_data()

  def load_data(self):
    with open('data.json') as json_file:
      data = json.load(json_file)
      self.data = data

    with open('file_size.json') as json_file:
      file_size = json.load(json_file)
      self.file_size = file_size

    cache_size = config['simulator']['cache']['size'] * 1024 * 1024
    policy = config['simulator']['cache']['policy']
    if policy == 'FIFO':
      self.policy =FIFO(cache_size, self.file_size, self.downloader)
    elif policy == 'LFU':
      self.policy = LFU(cache_size, self.file_size, self.downloader)
    elif policy == 'LRU':
      self.policy = LRU(cache_size, self.file_size, self.downloader)
    elif policy == 'RR':
      self.policy = RR(cache_size, self.file_size, self.downloader)
    elif policy == 'Belady':
      self.policy = Belady(cache_size, self.file_size, self.downloader, self.BeladyFreq)
    else:
      print('Wrong policy')
      os.exit(1)

  def calucate_cache_score(self, files):
    score = 0
    for file in files:
      if file in self.cache:
        score += 1
    
    return score / len(files)

  def get_avalaible_cpu(self):
    return self.cpu

  def mock_execute(self):
    print('Start mocking exectuion %d' % self.env.now)
    yield self.env.timeout(5000)
    print('End mocking exectuion %d' % self.env.now)

  def get_swap(self):
    return self.policy.get_swap_count()
    # swap_count_list = []
    # for policy in self.policies:
    #   swap_count_list.append(policy.get_swap_count())
    # return swap_count_list

  def get_hit(self):
    return self.policy.get_hit_count()
    # hit_count_list = []
    # for policy in self.policies:
    #   hit_count_list.append(policy.get_hit_count())
    # return hit_count_list

  def get_miss(self):
    return self.policy.get_miss_count()
    # miss_count_list = []
    # for policy in self.policies:
    #   miss_count_list.append(policy.get_miss_count())
    # return miss_count_list

  def get_download_size(self):
    return self.policy.get_download_size()
    # time_save_count_list = []
    # for policy in self.policies:
    #   time_save_count_list.append(policy.get_saved_time())
    # return time_save_count_list
  
  def get_full_download_size(self):
    return self.policy.get_full_download_size()
    # download_time_count_list = []
    # for policy in self.policies:
    #   download_time_count_list.append(policy.get_full_download_time())
    # return download_time_count_list

  def execute(self, job_id, msg):
    job = job_id.split(":")
    sleep_time = self.data[str(job[2])]["time"] / config['simulator']['divisor']
    self.cpu -= self.data[str(job[2])]["cpu"]

    for file in msg.get("ins"):
      if file == "length":
        break
      # for policy in self.policies:
      #   policy.process(msg.get("ins").get(file).get("name"), True)
      name = msg.get("ins").get(file).get("name")
      if config['simulator']['cache']['enabled']:
        self.policy.process(name, True)
      else:
        mock_download(self.file_size[name], self.downloader)

    time.sleep(sleep_time)

    for file in msg.get("outs"):
      if file == "length":
        break
      if config['simulator']['cache']['enabled']:
        self.policy.process(msg.get("outs").get(file).get("name"))

    self.cpu += self.data[str(job[2])]["cpu"]
      #self.memory += self.data[str(job[2])]["cpu"]
