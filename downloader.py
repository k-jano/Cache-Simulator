import time
import yaml
import uuid

config = yaml.safe_load(open("./config.yml"))

class Downloader():
  def __init__(self):
    self.jobs = {}
    self.old_jobs = {}
    self.bandwith = (config['simulator']['bandwith'] * 1024 * 1024 * 1024) / 8

  def create_job(self, file_size):
    job = {
      "size": file_size,
      "left": file_size,
      "time": 0
    }
    id = str(uuid.uuid4())
    self.jobs[id] = job
    return id

  def is_job_done(self, id):
    if id in self.old_jobs:
      return True
    return False

  def get_left_size(self, id):
    if id in self.old_jobs:
      return 0
    return self.jobs[id]['left']

  def routine(self):
    while True:
      time.sleep(1)

      #routine
      single_bandwith = self.bandwith / len(self.jobs.keys()) if len(self.jobs.keys()) > 0 else None

      for key in self.jobs.keys():
        job = self.jobs[key]
        job['left'] -= single_bandwith
        if job['left'] < 0:
          job['left'] = 0
        job['time'] += 1
        self.jobs[key] = job

      for key in self.jobs.copy():
        if self.jobs[key]['left'] <= 0:
          self.old_jobs[key] = self.jobs.pop(key, None)
