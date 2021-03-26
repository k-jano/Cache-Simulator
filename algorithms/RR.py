import random

class RR():

  def __init__(self, memory_size, files_size):
    self.MAX = 1000000
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.swap_count = 0
    self.files_size = files_size

  def process(self, file):
    file_size = self.files_size[file]

    if file in self.cache:
      return

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

  def get_swap_count(self):
    return self.swap_count
