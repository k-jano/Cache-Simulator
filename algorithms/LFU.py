class LFU():

  def __init__(self, memory_size, files_size, *args):
    self.name = 'LFU'
    self.MAX = 1000000
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.swap_count = 0
    self.files_size = files_size
    self.LFU_dict = {}
    self.hit_count = 0
    self.miss_count = 0
    for i in files_size:
      self.LFU_dict[i] = 0


  def process(self, file):
    file_size = self.files_size[file]

    self.LFU_dict[file] = self.LFU_dict[file] + 1

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
      LFU_elem = self.get_LFU()
      self.size -= self.files_size[LFU_elem]
      self.cache.remove(LFU_elem)
      self.swap_count += 1

    self.size += file_size
    self.cache.append(file)

  def get_LFU(self):
    LFU_elem = -1
    LFU_freq = self.MAX
    for file in self.cache:
      if self.LFU_dict[file] < LFU_freq:
        LFU_elem = file
        LFU_freq = self.LFU_dict[file]

    return LFU_elem

  def get_swap_count(self):
    return self.swap_count

  def get_hit_count(self):
    return self.hit_count

  def get_miss_count(self):
    return self.miss_count

  def get_name(self):
    return self.name