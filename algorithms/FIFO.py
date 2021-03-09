class FIFO():

  def __init__(self):
    self.queue = []
    
  def initialize(self, memory):
    self.queue = memory

  def swap(self, file):
    self.queue.append(file)
    self.queue.pop(0)
    return self.queue
