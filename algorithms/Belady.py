import json

from algorithms.policy import Policy
from helpers.mock_download import mock_download

class Belady(Policy):

  def __init__(self, memory_size, files_size, BeladyFreq, *args):
    super().__init__()
    self.name = 'Belady'
    self.MAX = 1000000
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.files_size = files_size
    self.path = "freq.json"
    self.step = 0
    self.belady_dict = {}
    self.load_order()
    self.BeladyFreq = BeladyFreq

  def load_order(self):
    f = open(self.path)
    self.freq = json.load(f)
    f.close()

  def process(self, file, is_in=False):
    file_size = self.files_size[file]
    self.acc_full_download_time(file_size) if is_in else None

    if file in self.cache:
      self.hit_count += 1 if is_in else 0
      self.acc_download_time(file_size) if is_in else None
      return

    self.miss_count +=1 if is_in else 0

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      self.cache.append(file)
    else:
      self.swap(file, file_size)

    mock_download(file_size) if is_in else None

  def swap(self, file, file_size):
    while self.size + file_size > self.memory_size:
      Belady_elem = self.get_Belady(file)
      self.size -= self.files_size[Belady_elem]
      self.cache.remove(Belady_elem)
      self.swap_count += 1

    self.size += file_size
    self.cache.append(file)
    self.BeladyFreq.decrement(file)

  def get_Belady(self, root_file):
    Belady_val = self.MAX
    Belady_elem = -1
    for file in self.cache:
      if self.BeladyFreq.get(file) < Belady_val:
        Belady_val = self.BeladyFreq.get(file)
        Belady_elem = file

    return Belady_elem
