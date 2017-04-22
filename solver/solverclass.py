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
		action, coordinates, value, wild_card = self.algorithm.execute(percepts)
		if(action == "resolve"):
			#raw_input(str(results[3]) + "adjusting: to " + str(self.actions))
			self.actions.remove(wild_card)# = self.actions[:self.actions.index(results[3])]
			#raw_input(self.actions)
		else:
			self.actions.append((action, coordinates, value, wild_card))
		return (action, coordinates, value, wild_card)


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

		for x in range(0,9):
			for y in range(0,9):
				# For numbers given, gives these slots an "infinite cost" to change
				if(self.reset_puzzle.visible_p[x][y] > 0):
					self.num_map[x][y] = []
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
			row = []
			for x in range(0 + (z/3 * 3),3 + (z/3 * 3)):
				for y in range(0 + (z%3) * 3,3 + (z%3) * 3):
					if(puzzle.visible_p[x][y] > 0 and puzzle.visible_p[x][y] < 10):
						row.append(puzzle.visible_p[x][y])
			
			for x in range(0 + (z/3 * 3),3 + (z/3 * 3)):
				for y in range(0 + (z%3) * 3,3 + (z%3) * 3):
					for a in row:
						if a in self.num_map[x][y]:
							self.num_map[x][y].remove(a)

	# scan using crosshatch to determine numbers
	def crosshatch(self):
		for z in range(0,9):
			square = []
			for x in range(0 + (z/3 * 3),3 + (z/3 * 3)):
				for y in range(0 + (z%3) * 3,3 + (z%3) * 3):
					square += self.num_map[x][y]
			# scan through 9 squares and replace the numbers in their map, splice the numbers already present in the checking square
			# remove it and place into square 2 (not implemented yet)
			for x in range(0 + (z/3 * 3),3 + (z/3 * 3)):
				for y in range(0 + (z%3) * 3,3 + (z%3) * 3):
					square2 = copy.deepcopy(square)
					for p in self.num_map[x][y]:
						if p in square2:
							square2.remove(p)
					for p in range(0,12):
						if (100 + p) in square2:
							square2.remove(100 + p)
					tmp = copy.deepcopy(self.num_map[x][y])
					for p in square2:
						if p in tmp:
							tmp.remove(p)
					if(len(tmp) > 0):
						if 100 in tmp:
							pass
						else:
							self.num_map[x][y] = copy.deepcopy(tmp)

	#from http://www.sudoku-solutions.com/index.php?page=solvingInteractions
	#implement pointing pairs techinques
	#T1: if candidate only TWICE is shared in row or column - remove from other cells (not implemented)
	#T2: if pair of empty cells share candidate AND that candidate does not appear in row or column - remove from all
	#other cells in square (not implemented)
	#T3: Pointing Triple (implementation necessary?)
	def pointing_pairs(self):
		# check for sharing per row in a square and remove from all others in the row
		# First square check
		# 
		#row count
		
		#scans 1 row in 1 square
		#
		#
		row = []
		# applies algorithm for rows of each square
		# checks for first 3 squares
		for p in range(0,1):
			row = []
			backup_row = None
			# get row of all squares
			for y in range(0,3):
				row.append(self.num_map[0][p*3 + y])
				row.append(self.num_map[1][p*3 + y])
				row.append(self.num_map[2][p*3 + y])
			backup_row = copy.deepcopy(row)

			raw_input("backup_row: " + str(backup_row[0]))

			for x in range(0,3):
				row = copy.deepcopy(backup_row)
				raw_input("before: " + str(row[x % 3]))
				for candidate in row[(x + 1) % 3]:
					if candidate in row[x % 3]:
						row[x % 3].remove(candidate)

				for candidate in row[(x + 2) % 3]:
					if candidate in row[x % 3]:
						row[x % 3].remove(candidate)

			# remove candidates left from row of other squares
				for y in range(3,9):
					for candidate in row[x % 3]:
						if candidate in self.num_map[x % 3][y]:
							self.num_map[x % 3][y].remove(candidate)
				raw_input("after: " + str(row[x % 3]))
		#self.print_nm_map()
		#raw_input("row0: " + str(row[2]))



	def print_nm_map(self):
		tmp = ""
		for x in range(0,9):
			for y in range(0,9):
				tmp += str((x,y)) + " " + str(self.num_map[x][y])
				tmp += "\n"
		print(tmp)

	# Only supports make a decision if there an array of length 1 e.g. given
	# Returns the actions to take they are as follows
	def make_decision(self, action_map):
		# decision algorithm
		minimum = 10
		coordinates = None
		#self.crosshatch()
		for x in range(0,9):
		#	# for testing it excludes last tile
			for y in range(0,9):
				if(len(self.num_map[x][y]) > 0 and len(self.num_map[x][y]) <= minimum):
					minimum = len(self.num_map[x][y])
					coordinates = (x,y)
		# no possible moves
		if(minimum == 10):
			return ("none", (0,0),0, 0)
		elif(minimum == 1):
			print("Possibilites: " + str(minimum) + " " + str(self.num_map[coordinates[0]][coordinates[1]]))
			return ("input", coordinates, self.num_map[coordinates[0]][coordinates[1]][0], 1.0 / len(self.num_map[coordinates[0]][coordinates[1]]))
		else:
			self.crosshatch()
			for x in range(0,9):
			#	# for testing it excludes last tile
				for y in range(0,9):
					if(len(self.num_map[x][y]) > 0 and len(self.num_map[x][y]) < minimum):
						minimum = len(self.num_map[x][y])
						coordinates = (x,y)
			if(minimum == 1):
				return ("input", coordinates, self.num_map[coordinates[0]][coordinates[1]][0], 1.0 / len(self.num_map[coordinates[0]][coordinates[1]]))
			else:
				self.pointing_pairs()
				self.print_nm_map()
				#raw_input("ran pointing pairs")
				return ("none", (0,0), 0, 0)
		return ("none", (0,0), 0, 0)


	def execute(self, data):
		puzzle, action_map = data
		self.update_map(puzzle)
		return self.make_decision(action_map)

# class to plug in the sudoku environment
class SEnvironment(Environment):
	def __init__(self, agent = None, puzzle = None):
		self.agent = agent
		self.puzzle = puzzle
		self.counter = 0

	# One step through simulation. Calls agent's execute and passes in the percepts from the percept
	# function
	def step(self):
		action, coordinates, value, probabilities = self.agent.execute(self.percepts())
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
		probabilities = self.agent.actions

		return (self.puzzle, probabilities)