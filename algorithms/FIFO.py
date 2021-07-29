from algorithms.policy import Policy
from helpers.mock_download import mock_download


class FIFO(Policy):

  def __init__(self, memory_size, files_size, *args):
    super().__init__()
    self.name = 'FIFO'
    self.memory_size = memory_size
    self.size = 0
    self.queue = []
    self.files_size = files_size

  def process(self, file, is_in=False):
    file_size = self.files_size[file]
    self.acc_full_download_time(file_size) if is_in else None

    if file in self.queue:
      self.hit_count+=1
      self.acc_download_time(file_size) if is_in else None
      return

    self.miss_count +=1

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      self.queue.append(file)
    else:
      self.swap(file, file_size)

    mock_download(file_size) if is_in else None

  def swap(self, file, file_size):
    while self.size + file_size > self.memory_size:
      self.size -= self.files_size[self.queue[0]]
      self.queue.pop(0)
      self.swap_count += 1

    self.size += file_size
    self.queue.append(file)
    return self.queue
