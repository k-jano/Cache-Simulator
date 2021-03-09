import json

from algorithms.FIFO import FIFO

class SwapAlgorithmEvalutor():

  def __init__(self):
    self.load_data()
    self.count = 0
    self.memory = []
    self.swap_count = 0
    self.algorithm = FIFO()
    self.initialized = False

  def load_data(self):
    with open('data.json') as json_file:
      data = json.load(json_file)
      self.memory_count = data['memory_count']
      self.file_count = data['file_count']
      self.order = data['order']

  def process_workflow(self):
    for file in self.order:
      if self.count < self.memory_count:
        self.memory.append(file)
        self.memory = list(set(self.memory))
        self.count += 1
      else:
        if not self.initialized:
          self.algorithm.initialize(self.memory)
          self.initialized = True

        if not file in self.memory:
          self.memory = self.algorithm.swap(file)
          self.swap_count +=1

    print("Swap count: ", self.swap_count)

if __name__ == '__main__':
  SAEvaluator = SwapAlgorithmEvalutor()
  SAEvaluator.process_workflow()
