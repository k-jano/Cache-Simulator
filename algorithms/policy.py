# import time
from abc import ABC
import yaml

config = yaml.safe_load(open("./config.yml"))

class Policy(ABC):
  def __init__(self):
    self.download_size = 0
    self.full_download_size = 0
    self.hit_count = 0
    self.miss_count = 0
    self.swap_count = 0
    self.bandwith = (config['simulator']['bandwith'] * 1024 * 1024) / 8
    self.delay = config['simulator']['delay']
    self.downloads = {}
    
  def acc_download_size(self, file_size):
    self.download_size += file_size

  def acc_full_download_size(self, file_size):
    self.full_download_size += file_size

  # def mock_download(self, file_size):
  #   time.sleep(file_size / self.bandwith + self.delay)

  def get_swap_count(self):
    return self.swap_count

  def get_hit_count(self):
    return self.hit_count

  def get_miss_count(self):
    return self.miss_count

  def get_name(self):
    return self.name

  def get_download_size(self):
    return self.download_size

  def get_full_download_size(self):
    return self.full_download_size
