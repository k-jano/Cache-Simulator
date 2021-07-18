import random

from algorithms.policy import Policy

class RR(Policy):

  def __init__(self, memory_size, files_size, *args):
    super().__init__()
    self.name = 'RR'
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.files_size = files_size

  def process(self, file):
    file_size = self.files_size[file]
    self.acc_full_download_time(file_size)

    if file in self.cache:
      self.hit_count += 1
      self.acc_download_time(file_size)
      return

    self.miss_count += 1
    if self.size + file_size <= self.memory_size:
      self.size += file_size
      self.cache.append(file)
    else:
      self.swap(file, file_size)

  def swap(self, file, file_size):
    while self.size + file_size > self.memory_size:
      RR_elem = self.get_RR()
      self.size -= self.files_size[RR_elem]
      self.cache.remove(RR_elem)
      self.swap_count += 1

    self.size += file_size
    self.cache.append(file)

  def get_RR(self):
    return random.choice(self.cache)
