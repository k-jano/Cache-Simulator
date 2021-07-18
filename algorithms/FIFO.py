import yaml

config = yaml.safe_load(open("./config.yml"))

class FIFO():

  def __init__(self, memory_size, files_size, *args):
    self.name = 'FIFO'
    self.memory_size = memory_size
    self.size = 0
    self.queue = []
    self.swap_count = 0
    self.files_size = files_size
    self.hit_count = 0
    self.miss_count = 0
    self.bandwith = (config['simulator']['bandwith'] * 1024 * 1024) / 8
    self.time_saved = 0

  def acc_download_time(self, file_size):
    self.time_saved += file_size / self.bandwith

  def process(self, file):
    file_size = self.files_size[file]

    if file in self.queue:
      self.hit_count+=1
      self.acc_download_time(file_size)
      return

    self.miss_count +=1

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      self.queue.append(file)
    else:
      self.swap(file, file_size)

  def swap(self, file, file_size):
    while self.size + file_size > self.memory_size:
      self.size -= self.files_size[self.queue[0]]
      self.queue.pop(0)
      self.swap_count += 1

    self.size += file_size
    self.queue.append(file)
    return self.queue


  def get_swap_count(self):
    return self.swap_count

  def get_hit_count(self):
    return self.hit_count

  def get_miss_count(self):
    return self.miss_count

  def get_name(self):
    return self.name

  def get_saved_time(self):
    return self.time_saved
