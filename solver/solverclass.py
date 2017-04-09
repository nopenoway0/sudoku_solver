from templates import *
# Sudoku Agent
class SAgent(Agent):
	def __init__(self, algorithm = None, kb = None):
		# Algorithm to run for each step of the agent
		self.algorithm = algorithm

		# Knowledge based. Use PyKe or something else?
		self.kb = kb

	# simply calls algorithms execute method. Can alter any self variables that we add as well
	def execute(self, percepts):
		self.algorithm.execute(percepts)

# class that will contain algorithm to navigate sudoku board. Incoming percepts should be:
# 	current sudoku puzzle
# 	probabilities calculated through machine learning
class SRuleAlgorithm:
	def execute(self, percepts):
		# action = change, input, or error
		# change is for when the current value present in the table must be changed
		# input is for a blank slot
		# error, the algorithm failed
		# Coordinates are the grid affect and the value is what the grid will be changed
		# into
		
		# Place holder
		puzzle, probabilities = percepts
		action, coordinates, value = (None, (0,0), 0)
		# Algorithm goes here
		# 
		# 
		return (action, coordinates, value)

# class to plug in the sudoku environment
class SEnvironment:
	def __init__(self, agent = None, puzzle = None):
		self.agent = agent
		self.puzzle = puzzle
		self.counter = 0

	# One step through simulation. Calls agent's execute and passes in the percepts from the percept
	# function
	def step(self):
		self.agent.execute(self.percepts())

	def percepts(self):
		#
		# Calculate probabilities based on previous experiences
		#
		probabilities = 0

		return (self.puzzle, probabilities)