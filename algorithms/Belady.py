class Belady():

  def __init__(self, memory_size, files_size, order):
    self.MAX = 1000000
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.swap_count = 0
    self.files_size = files_size
    self.order = order
    self.step = 0
    self.belady_dict = {}

  def process(self, file):
    file_size = self.files_size[file]

    self.step+=1

    try:
      self.belady_dict[file] = self.order.index(file, self.step)
    except ValueError:
      self.belady_dict[file] = self.MAX

    if file in self.cache:
      return

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      self.cache.append(file)
    else:
      self.swap(file, file_size)

  def swap(self, file, file_size):
    while self.size + file_size > self.memory_size:
      Belady_elem = self.get_Belady()
      self.size -= self.files_size[Belady_elem]
      self.cache.remove(Belady_elem)
      self.swap_count += 1

    self.size += file_size
    self.cache.append(file)

  def get_Belady(self):
    Belady_elem = -1
    Belady_time = -1
    for file in self.cache:
      if self.belady_dict[file] > Belady_time:
        Belady_elem = file
        Belady_time = self.belady_dict[file]

    return Belady_elem

  def get_swap_count(self):
    return self.swap_count
