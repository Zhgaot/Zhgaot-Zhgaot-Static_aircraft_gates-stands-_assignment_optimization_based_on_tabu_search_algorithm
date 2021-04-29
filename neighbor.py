
class Neighbor:
	def __init__(self, nb_sol, f, g1, g2):
		self.neighbor = nb_sol
		self.f1 = f
		self.old_gate_f1 = g1
		self.new_gate_f1 = g2
		self.f2 = -1
		self.old_gate_f2 = -1
		self.new_gate_f2 = -1

	def add_swap(self, f2, g1_2, g2_2):
		self.f2 = f2
		self.old_gate_f2 = g1_2
		self.new_gate_f2 = g2_2
