class s_FIFO():

  def __init__(self, files_count_max, *args):
    self.name = 'FIFO'
    self.queue = []
    self.swap_count = 0
    self.count = 0
    self.files_count_max = files_count_max


  def process(self, file):
    file_size = self.files_size[file]

    if file in self.queue:
      return

    if self.count + 1 <= self.files_count_max:
      self.size += 1
    else:
      self.queue.pop(0)
      self.swap_count += 1

    self.queue.append(file)

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

  def get_name(self):
    return self.name