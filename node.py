class Node():
  def __init__(self, id):
    self.cache = []
    self.vcpu = 10
    self.id = id

  def get_avalaible_vcpu(self):
    return self.vcpu
