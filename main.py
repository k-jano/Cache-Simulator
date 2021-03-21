import json

from algorithms.FIFO import FIFO

class SwapAlgorithmEvalutor():

  def __init__(self):
    self.memory = []
    self.swap_count = 0
    self.algorithm = None

  def load_data(self):
    with open('data.json') as json_file:
      data = json.load(json_file)
      self.memory_size = data['memory_size']
      self.file_count = data['file_count']
      self.files_size = data['files_size']
      self.order = data['order']

    self.algorithm = FIFO(self.memory_size, self.files_size)

  def process_workflow(self):
    for file in self.order:
      self.algorithm.process(file)

    print("Swap count: ", self.algorithm.get_swap_count())

if __name__ == '__main__':
  SAEvaluator = SwapAlgorithmEvalutor()
  SAEvaluator.load_data()
  SAEvaluator.process_workflow()
