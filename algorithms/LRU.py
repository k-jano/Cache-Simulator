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
    for i in range(len(files_size)):
      self.LRU_dict[i] = -1


  def process(self, file):
    file_size = self.files_size[file]

    self.LRU_dict[file] = self.time_counter
    self.time_counter += 1

    if file in self.cache:
      return

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

  def get_name(self):
    return self.name
