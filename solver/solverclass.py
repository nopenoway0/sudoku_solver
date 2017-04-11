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
class SRuleAlgorithm(Algorithm):
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

class BruteAlgorithm(Algorithm):
	def __init__(self, puzzle):
		self.num_map = []

		for x in range(0,9):
			self.num_map.append([])
			for y in range(0,9):
				self.num_map[x].append([])
				#self.num_map[x][y].append([]) don't think this is needed

		for x in range(0,9):
			for y in range(0,9):
				# For numbers given, gives these slots an "infinite cost" to change
				if(puzzle.visible_p[x][y] > 0):
					for z in range(0,10):
						self.num_map[x][y].append(100)
				else:
					for z in range(1,10):
						self.num_map[x][y].append(z)

	def execute(self, data):
		puzzle, probabilities = data
		row = []
		# Calculate possible numbers based of numbers in row
		for x in range(0,9):
			row = []
			for y in range(0,9):
				if(puzzle.visible_p[x][y] > 0 and puzzle.visible_p[x][y] < 10):
					row.append(puzzle.visible_p[x][y])
			for y in range(0,9):
				for z in row:
					if z in self.num_map[x][y]:
						self.num_map[x][y].remove(z)

		# Calculate possible numbers based on numbers in columns
		for y in range(0,9):
			row = []
			for x in range(0,9):
				if(puzzle.visible_p[x][y] > 0 and puzzle.visible_p[x][y] < 10):
					row.append(puzzle.visible_p[x][y])
			for x in range(0,9):
				for z in row:
					if z in self.num_map[x][y]:
						self.num_map[x][y].remove(z)

		# Add check for possible numbers based off squares

# class to plug in the sudoku environment
class SEnvironment(Environment):
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