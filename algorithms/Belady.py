import json

class Belady():

  def __init__(self, memory_size, files_size, BeladyFreq, *args):
    self.name = 'Belady'
    self.MAX = 1000000
    self.memory_size = memory_size
    self.size = 0
    self.cache = []
    self.swap_count = 0
    self.files_size = files_size
    #.order = order
    self.path = "freq.json"
    self.step = 0
    self.belady_dict = {}
    self.load_order()
    self.hit_count = 0
    self.miss_count = 0
    self.BeladyFreq = BeladyFreq

  def load_order(self):
    f = open(self.path)
    self.freq = json.load(f)
    f.close()

  def process(self, file):
    file_size = self.files_size[file]

    #self.step+=1

    # try:
    #   self.belady_dict[file] = self.order.index(file, self.step)
    # except ValueError:
    #   self.belady_dict[file] = self.MAX

    if file in self.cache:
      self.hit_count += 1
      return

    self.miss_count +=1

    if self.size + file_size <= self.memory_size:
      self.size += file_size
      self.cache.append(file)
    else:
      self.swap(file, file_size)

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
    # Belady_elem = -1
    # Belady_time = -1
    # for file in self.cache:
    #   #if self.belady_dict[root_file][file] = 
    #   distance = self.order[root_file][file]
    #   if distance > Belady_time or distance == -1:
    #     Belady_elem = file
    #     if distance == -1:
    #       Belady_time = self.MAX
    #     Belady_time = distance

    Belady_val = self.MAX
    Belady_elem = -1
    for file in self.cache:
      if self.BeladyFreq.get(file) < Belady_val:
        Belady_val = self.BeladyFreq.get(file)
        Belady_elem = file
      # if self.freq[file] < Belady_val:
      #   Belady_val = self.freq[file]
      #   Belady_elem = file

    return Belady_elem

  def get_swap_count(self):
    return self.swap_count

  def get_hit_count(self):
    return self.hit_count

  def get_miss_count(self):
    return self.miss_count

  def get_name(self):
    return self.name
