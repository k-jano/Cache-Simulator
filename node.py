import time
import json

class Node():
  def __init__(self, id):
    self.cache = []
    self.vcpu = 10
    self.id = id
    self.data = None

    self.load_data()

  def load_data(self):
    with open('data.json') as json_file:
      data = json.load(json_file)
      self.data = data

  def get_avalaible_vcpu(self):
    return self.vcpu

  def execute(self, job_id):
    job = job_id.split(":")
    sleep_time = self.data.get(job[1])[int(job[2])]
    time.sleep(sleep_time)
