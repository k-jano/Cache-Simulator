from algorithms.policy import Policy
from helpers.mock_download import mock_download

class LRU(Policy):

  def __init__(self, memory_size, files_size, *args):
    super().__init__()
    self.name = 'LRU'
    self.MAX = 1000000
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.files_size = files_size
    self.time_counter = 0
    self.LRU_dict = {}
    for i in files_size:
      self.LRU_dict[i] = -1

  def process(self, file, is_in=False):
    file_size = self.files_size[file]
    self.acc_full_download_time(file_size) if is_in else None
    self.LRU_dict[file] = self.time_counter
    self.time_counter += 1

    if file in self.cache:
      self.hit_count += 1
      self.acc_download_time(file_size) if is_in else None
      return

    self.miss_count += 1

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      self.cache.append(file)
    else:
      self.swap(file, file_size)

    mock_download(file_size) if is_in else None

  def swap(self, file, file_size):
    while self.size + file_size > self.memory_size:
      LRU_elem = self.get_LRU()
      self.size -= self.files_size[LRU_elem]
      self.cache.remove(LRU_elem)
      self.swap_count += 1

    self.size += file_size
    self.cache.append(file)

  def get_LRU(self):
    LRU_elem = -1
    LRU_time = self.MAX
    for file in self.cache:
      if self.LRU_dict[file] < LRU_time:
        LRU_elem = file
        LRU_time = self.LRU_dict[file]

    return LRU_elem
