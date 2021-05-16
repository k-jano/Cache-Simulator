import time
import json
import simpy

class Node():
  def __init__(self, id):
    self.cache = []
    self.vcpu = 10
    self.id = id
    self.data = None
    self.env = simpy.Environment()

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

  def execute(self, job_id):
    job = job_id.split(":")
    sleep_time = self.data.get('time')[int(job[2])-1]
    time.sleep(sleep_time)
