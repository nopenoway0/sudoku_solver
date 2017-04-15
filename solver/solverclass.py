from templates import *
import random
import copy
# Sudoku Agent
class SAgent(Agent):
	def __init__(self, algorithm = None, kb = None):
		# Algorithm to run for each step of the agent
		self.algorithm = algorithm
		self.actions = []
		# Knowledge based. Use PyKe or something else?
		self.kb = kb

	# simply calls algorithms execute method. Can alter any self variables that we add as well
	def execute(self, percepts):
		results = self.algorithm.execute(percepts)
		self.actions.append(results)
		return results


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

class NakedCandidateAlgorithm(Algorithm):
	def __init__(self, puzzle):
		self.num_map = []
		self.reset_puzzle = copy.deepcopy(puzzle) 
		self.reset()

	def reset(self):
		for x in range(0,9):
			self.num_map.append([])
			for y in range(0,9):
				self.num_map[x].append([])
				#self.num_map[x][y].append([]) don't think this is needed

		for x in range(0,9):
			for y in range(0,9):
				# For numbers given, gives these slots an "infinite cost" to change
				if(self.reset_puzzle.visible_p[x][y] > 0):
					for z in range(0,12):
						self.num_map[x][y].append(100 + z)
				else:
					for z in range(1,10):
						self.num_map[x][y].append(z)

	def update_map(self, puzzle):
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
		for z in range(0,9):
			test = ""
			row = []
			for x in range(0 + (z/3 * 3),3 + (z/3 * 3)):
				for y in range(0 + (z%3) * 3,3 + (z%3) * 3):
					if(puzzle.visible_p[x][y] > 0 and puzzle.visible_p[x][y] < 10):
						row.append(puzzle.visible_p[x][y])
						#test += str((x,y)) + str(puzzle.visible_p[x][y]) + " "
					#else:
					#	test += str((x,y)) + "- "
					#test += "counter, z: " + str(((z%3)*3, z))
				#test += "\n"
			
			for x in range(0 + (z/3 * 3),3 + (z/3 * 3)):
				for y in range(0 + (z%3) * 3,3 + (z%3) * 3):
					for a in row:
						if a in self.num_map[x][y]:
							self.num_map[x][y].remove(a)
			#print(test)
	def print_nm_map(self):
		tmp = ""
		for x in range(0,9):
			for y in range(0,9):
				tmp += str((x,y)) + " " + str(self.num_map[x][y])
				tmp += "\n"
		print(tmp)

	# Only supports make a decision if there an array of length 1 e.g. given
	# Returns the actions to take they are as follows
	def make_decision(self):
		# decision algorithm
		minimum = 10
		coordinates = None
		for x in range(0,9):
			# for testing it excludes last tile
			for y in range(0,9):
				if(len(self.num_map[x][y]) > 0 and len(self.num_map[x][y]) < minimum):
					minimum = len(self.num_map[x][y])
					coordinates = (x,y)
		# Random attempt to resolve conflict in puzzle
		if(minimum == 10):
			#return ("done", (0,0), 0)
			self.reset()
			# set a random space to 0 and attempt to try again
			return ("input", (random.randrange(0, 9), random.randrange(0,9)), 0)
		else:
			print("Possibilites: " + str(minimum) + " " + str(self.num_map[coordinates[0]][coordinates[1]]))
			return ("input", coordinates, self.num_map[coordinates[0]][coordinates[1]][random.randrange(0, len(self.num_map[coordinates[0]][coordinates[1]]))])
		return ("none", (0,0), 0)


	def execute(self, data):
		puzzle, probabilities = data
		self.update_map(puzzle)
		return self.make_decision()

# class to plug in the sudoku environment
class SEnvironment(Environment):
	def __init__(self, agent = None, puzzle = None):
		self.agent = agent
		self.puzzle = puzzle
		self.counter = 0

	# One step through simulation. Calls agent's execute and passes in the percepts from the percept
	# function
	def step(self):
		action, coordinates, value = self.agent.execute(self.percepts())
		if(self.execute(action, coordinates, value)):
			return True

	def execute(self, action, coordinates, value):
		print("perform: %s at row: %d column: %d to %d" % (action, coordinates[0], coordinates[1], value))
		if(action == "input"):
			self.puzzle.execute("%d-%d %d" % (coordinates[0], coordinates[1], value))
		if(action == "error"):
			raise Exception("Can't do anything")
		if(action == "done"):
			return True

	def percepts(self):
		#
		# Calculate probabilities based on previous experiences
		#
		probabilities = 0

		return (self.puzzle, probabilities)