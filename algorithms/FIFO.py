from algorithms.policy import Policy
from helpers.mock_download import mock_download
import time

class FIFO(Policy):

  def __init__(self, memory_size, files_size, downloader, *args):
    super().__init__()
    self.name = 'FIFO'
    self.memory_size = memory_size
    self.size = 0
    self.queue = []
    self.files_size = files_size
    self.downloader = downloader


  def process(self, file, is_in=False):
    file_size = self.files_size[file]
    self.acc_full_download_size(file_size) if is_in else None

    if file in self.queue:
      self.hit_count+=1 if is_in else 0
      job_id = self.downloads[file]
      self.acc_download_size(self.downloader.get_left_size(job_id))
      while not self.downloader.is_job_done(job_id):
        time.sleep(1)
      return

    self.miss_count +=1 if is_in else 0

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      #self.queue.append(file)
    else:
      self.swap(file, file_size)

    if is_in:
      job_id = self.downloader.create_job(file_size)
      self.downloads[file] = job_id
      self.queue.append(file)
      while not self.downloader.is_job_done(job_id):
        time.sleep(1)

  def swap(self, file, file_size):
    while self.size + file_size > self.memory_size:
      self.size -= self.files_size[self.queue[0]]
      self.queue.pop(0)
      self.swap_count += 1

    self.size += file_size
    #self.queue.append(file)
    return self.queue
