from algorithms.policy import Policy
from helpers.mock_download import mock_download
import time
import threading

class LFU(Policy):

  def __init__(self, memory_size, files_size, downloader, *args):
    super().__init__()
    self.name = 'LFU'
    self.MAX = 1000000
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.files_size = files_size
    self.LFU_dict = {}
    self.downloader = downloader
    self.lock = threading.Lock()
    for i in files_size:
      self.LFU_dict[i] = 0

  def process(self, file, is_in=False):
    file_size = self.files_size[file]
    self.acc_full_download_size(file_size) if is_in else None
    self.LFU_dict[file] = self.LFU_dict[file] + 1

    if file in self.cache:
      self.hit_count += 1 if is_in else 0
      job_id = self.downloads[file]
      self.acc_download_size(self.downloader.get_left_size(job_id))
      downlaoded = self.downloader.is_job_done(job_id)
      while not self.downloader.is_job_done(job_id):
        time.sleep(1)
      time.sleep(self.delay) if not downlaoded else None
      return

    self.miss_count += 1 if is_in else 0

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      #self.cache.append(file)
    else:
      self.swap(file, file_size)

    if is_in:
      job_id = self.downloader.create_job(file_size)
      self.downloads[file] = job_id
      self.cache.append(file)
      while not self.downloader.is_job_done(job_id):
        time.sleep(1)
      time.sleep(self.delay)

  def swap(self, file, file_size):
    while self.size + file_size > self.memory_size:
      self.lock.acquire()
      LFU_elem = self.get_LFU()
      self.size -= self.files_size[LFU_elem]
      self.cache.remove(LFU_elem)
      self.swap_count += 1
      self.lock.release()

    self.size += file_size
    #self.cache.append(file)

  def get_LFU(self):
    LFU_elem = -1
    LFU_freq = self.MAX
    for file in self.cache:
      if self.LFU_dict[file] < LFU_freq:
        LFU_elem = file
        LFU_freq = self.LFU_dict[file]

    return LFU_elem
