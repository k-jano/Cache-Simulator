class LRU():

  def __init__(self, memory_size, files_size, *args):
    self.name = 'LRU'
    self.MAX = 1000000
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.swap_count = 0
    self.files_size = files_size
    self.time_counter = 0
    self.LRU_dict = {}
    self.hit_count = 0
    self.miss_count = 0
    for i in files_size:
      self.LRU_dict[i] = -1


  def process(self, file):
    file_size = self.files_size[file]

    self.LRU_dict[file] = self.time_counter
    self.time_counter += 1

    if file in self.cache:
      self.hit_count += 1
      return

    self.miss_count += 1

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      self.cache.append(file)
    else:
      self.swap(file, file_size)

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

  def get_swap_count(self):
    return self.swap_count

  def get_hit_count(self):
    return self.hit_count

  def get_miss_count(self):
    return self.miss_count

  def get_name(self):
    return self.name
