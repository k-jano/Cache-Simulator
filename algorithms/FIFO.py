class FIFO():

  def __init__(self, memory_size, files_size):
    self.memory_size = memory_size
    self.size = 0
    self.queue = []
    self.swap_count = 0
    self.files_size = files_size


  def process(self, file):
    file_size = self.files_size[file]

    if file in self.queue:
      return

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