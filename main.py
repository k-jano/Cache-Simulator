import json

from algorithms.FIFO import FIFO
from algorithms.LRU import LRU
from algorithms.LFU import LFU
from algorithms.RR import RR
from algorithms.Belady import Belady

eval_algorithms = [FIFO, LRU, LFU, RR, Belady]

class SwapAlgorithmEvalutor():

  def __init__(self, algorithm_class):
    self.memory = []
    self.swap_count = 0
    self.algorithm = None
    self.algorithm_class = algorithm_class

  def load_data(self):
    with open('data.json') as json_file:
      data = json.load(json_file)
      self.memory_size = data['memory_size']
      self.file_count = data['file_count']
      self.files_size = data['files_size']
      self.order = data['order']

    self.algorithm = self.algorithm_class(self.memory_size, self.files_size, self.order)

  def process_workflow(self):
    for file in self.order:
      self.algorithm.process(file)

    print("[%s] Swap count: %d" % (self.algorithm.get_name(), self.algorithm.get_swap_count()))

if __name__ == '__main__':
  for algorithm in eval_algorithms:
    SAEvaluator = SwapAlgorithmEvalutor(algorithm)
    SAEvaluator.load_data()
    SAEvaluator.process_workflow()
