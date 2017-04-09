class Agent:
	def __init__(self):
		self.algorithm = None
		self.kb = None
	def execute(self, percepts):
		raise NotImplemented()

class Algorithm:
	def execute(self, percepts):
		raise NotImplemented()

class Environment:
	def __init__(self):
		self.agent = None

	def step(self):
		raise NotImplemented()