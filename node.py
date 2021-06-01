import time
import json
import simpy

from algorithms.s_FIFO import s_FIFO

class Node():
  def __init__(self, id):
    self.cache = []
    self.vcpu = 100
    self.memory = 1000000
    self.id = id
    self.data = None
    self.env = simpy.Environment()
    self.policy = s_FIFO(100)

    self.load_data()

  def load_data(self):
    with open('data.json') as json_file:
      data = json.load(json_file)
      self.data = data

  def get_avalaible_vcpu(self):
    return self.vcpu

  def mock_execute(self):
    print('Start mocking exectuion %d' % self.env.now)
    yield self.env.timeout(5000)
    print('End mocking exectuion %d' % self.env.now)

  def execute(self, job_id, msg):
    job = job_id.split(":")
    sleep_time = self.data[str(job[2])]["time"]
    #sleep_time = 0.001
    self.vcpu -= self.data[str(job[2])]["cpu"]
    self.memory -= self.data[str(job[2])]["cpu"]

    # for file in msg.get("ins"):
    #   self.policy.process(file)

    time.sleep(sleep_time)

    # for file in msg.get("ins"):
    #   self.policy.process(file)

    self.vcpu += self.data[str(job[2])]["cpu"]
    self.memory += self.data[str(job[2])]["cpu"]
