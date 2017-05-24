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
			self.actions.remove(wild_card)
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

		# can store stack here and use it for back tracking possibly - DONE
		self.movesStack = []

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

	# only row is currently implemented. must add column
	def hidden_candidate(self):
		for x in range(0,9):
			counter_row = []
			counter_col = []
			for y in range(0,10):
				counter_row.append(0)
				counter_col.append(0)
			for y in range(0,9):
				for z in self.num_map[x][y]:
					if(z < 10):
						counter_row[z] += 1
				for z in self.num_map[y][x]:
					if(z < 10):
						counter_col[z] += 1
			for y in range(0,10):
				if(counter_row[y] == 1):
					for z in range(0,9):
						if y in self.num_map[x][z]:
							self.num_map[x][z] = []
							self.num_map[x][z].append(y)
				elif(counter_col[y] == 1):
					for z in range(0,9):
						if y in self.num_map[z][x]:
							self.num_map[z][x] = []
							self.num_map[z][x].append(y)


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


	#my idea for backtracking
	#functions to create: backtrack, checkValiditiy
	#
	#We store the coordinates from make_decision into list
	#
	#Each time make_decision makes a decision, we checkValidity to see if
	#move is valid
	#If Move is not valid, we call backTracking to blank out last move
	#
	#todo: confirm on where to checkValidity and backTrack inside make_decision
	#      backtrack/checkValidity are probably broken...

	def backtrack(self):
		recentMove = movesStack.pop()
		x = recentMove.x
		y = recentMove.y
		#####
		#remove recent candidate from list
		self.num_map[x][y].remove(recentMove)
		new_guess = Candidate_Prediction
		#####
		return recentMove



	def checkValidity(self):
		n = len(num_map)
		digit = 1
		while digit <= n:
			i = 0
			while i < n:
				row_count = 0
				col_count = 0
				j = 0
				while j < n:
					if num_map[i][j] == digit:
						row_count = row_count + 1
					if num_map[j][i] == digit:
						col_count = col_count + 1
					j = j + 1
				if row_count != 1 or col_count != 1:
					return False
				i = i + 1
			digit  = digit + 1
		return True
	
	#this is made with assumption that false candidate is removed in backtrack
        #call method if two or more candidates are called 
        def Candidate_Prediction(self):
        	candidate = self.num_map[x][y]
        	guess_attempt_value = 0
        	#compare values
            	for i in len(candidates):
                	if(guess_attempt_value < candidate_score[candidate[i]]):
           	         	guess_attempt = candidate[i]
		if(guess_attempt != recentMove):
                	candidate_score[recentMove] -= 100
            	else:
               		candidate_score[guess_attempt] += 50
            	return guess_attempt
	
	# Learning + Backtracking will replace this
	#from http://www.sudoku-solutions.com/index.php?page=solvingInteractions
	#implement pointing pairs techinques
	#T1: if candidate only TWICE is shared in row or column - remove from other cells (not implemented)
	#T2: if pair of empty cells share candidate AND that candidate does not appear in row or column - remove from all
	#other cells in square (not implemented)
	#T3: Pointing Triple (implementation necessary?)
	def pointing_pairs(self):
		# applies algorithm for rows of each square
		# checks for first 3 squares
		for p in range(0,3):
			column = []
			row = []
			backup_row = None
			backup_col = None
			# get row of all squares
			for y in range(0,3):
				if(y == 0):
					row.append(copy.deepcopy(self.num_map[p/3 * 3 + 0][p*3 + y]))
					row.append(copy.deepcopy(self.num_map[p/3 * 3 + 1][p*3 + y]))
					row.append(copy.deepcopy(self.num_map[p/3 * 3 + 2][p*3 + y]))
				else:
					row[0] += copy.deepcopy(self.num_map[p/3 * 3 + 0][p*3 + y])
					row[1] += copy.deepcopy(self.num_map[p/3 * 3 + 1][p*3 + y])
					row[2] += copy.deepcopy(self.num_map[p/3 * 3 + 1][p*3 + y])

				if(y == 0):
					column.append(copy.deepcopy(self.num_map[(p%3) * 3 + y][p/3 * 3 + 0]))
					column.append(copy.deepcopy(self.num_map[(p%3) * 3 + y][p/3 * 3 + 1]))
					column.append(copy.deepcopy(self.num_map[(p%3) * 3 + y][p/3 * 3 + 2]))
				else:
					column[0] += copy.deepcopy(self.num_map[(p%3) * 3 + y][p/3 * 3 + 0])
					column[1] += copy.deepcopy(self.num_map[(p%3) * 3 + y][p/3 * 3 + 1])
					column[2] += copy.deepcopy(self.num_map[(p%3) * 3 + y][p/3 * 3 + 2])

			# remove duplicates for testing and legibility
			for x in range(0,3):
				row[x] = list(set(row[x]))
				for z in range(0,10):
					if (z + 100) in row[x]:
						row[x].remove(z + 100)
					if (z + 100) in column[x]:
						column[x].remove(z + 100)
				column[x] = list(set(column[x]))

			#make copies so we don't have to run those loops until the next square
			backup_row = copy.deepcopy(row)
			backup_col = copy.deepcopy(column)


			# Fix rows of first square
			for x in range(0,3):
				row = copy.deepcopy(backup_row)
				column = copy.deepcopy(backup_col)
				# modify row list
				for candidate in row[(x + 1) % 3]:
					if candidate in row[x % 3]:
						row[x % 3].remove(candidate)
				for candidate in row[(x + 2) % 3]:
					if candidate in row[x % 3]:
						row[x % 3].remove(candidate)

				# modify column list
				for candidate in column[(x + 1) % 3]:
					if candidate in column[x % 3]:
						column[x % 3].remove(candidate)
						column[x % 3].remove(candidate)

			# remove candidates left from row of other squares
				for y in range(0,6):
					count = 0
					for candidate in row[x]:
						if (candidate > 9):
							pass
						else:
							#check if the candidate only appears once in the row. If so, set it to the square
							for elem in self.num_map[(p%3) * 3 + x][(p*3 + 3 + y) % 9]:
								if(candidate == elem):
									count += 1
							if(count == 1 and len(row[x]) == 1):
								if 100 not in self.num_map[((p%3) * 3 + x)][(p*3 + y) % 9]:
									self.num_map[((p%3) * 3 + x)][(p*3 + y) % 9] = []
									self.num_map[((p%3) * 3 + x)][(p*3 + y) % 9].append(candidate)
							# if not remove from the rest of the of the rows
							else:
								if candidate in self.num_map[((p%3) * 3 + x)][(p*3 + 3 + y) % 9]:
									self.num_map[((p%3) * 3 + x)][(p*3 + 3 + y) % 9].remove(candidate)

					#do the same for columns. Not reducing candidates currently
					count = 0
					for candidate in column[x]:
						if (candidate > 9):
							pass#raw_input("can't remove " + str(candidate) + " from square" + str(p) + " at " + str(((p*3 + 3 + y) % 9, ((p%3) * 3 + x))))
						else:
							#check if the candidate only appears once in the column. If so, set it to the square
							for elem in self.num_map[(p*3 + 3 + y) % 9][(p%3) * 3 + x]:
								if(candidate == elem):
									count += 1
							if(count == 1 and len(column[x]) == 1):
								pass

							# if not remove from the rest of the of the columns
							else:
								if candidate in self.num_map[(p*3 + y) % 9][((p%3) * 3 + x)]:
									if (len(self.num_map[(p*3 + y) % 9][((p%3) * 3 + x)]) > 1):
										pass

	# Prints the array of containing all current candidates for each cell
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
		# scan for a cell that has only 1 possible candidate
		for x in range(0,9):
			for y in range(0,9):
				if(len(self.num_map[x][y]) > 0 and len(self.num_map[x][y]) <= minimum):
					minimum = len(self.num_map[x][y])
					coordinates = (x,y)
					#movesStack.append(coordinates) - dunno
		# no possible moves
		if(minimum == 10):
			return ("done", (0,0),0, 0)
		elif(minimum == 1):
			#print("Possibilites: " + str(minimum) + " " + str(self.num_map[coordinates[0]][coordinates[1]]))
			return ("input", coordinates, self.num_map[coordinates[0]][coordinates[1]][0], 1.0 / len(self.num_map[coordinates[0]][coordinates[1]]))
		else:
			self.crosshatch()
			#self.pointing_pairs() - don't use
			self.hidden_candidate()
			for x in range(0,9):
			#	# for testing it excludes last tile
				for y in range(0,9):
					if(len(self.num_map[x][y]) > 0 and len(self.num_map[x][y]) < minimum):
						minimum = len(self.num_map[x][y])
						coordinates = (x,y)

			if(minimum == 1):
				valueIn = self.num_map[coordinates[0]][coordinates[1]][0]
				self.movesStack.append(coordinates)
				return ("input", coordinates, valueIn, 1.0 / len(self.num_map[coordinates[0]][coordinates[1]]))
			else:
				#call backtrack here
				#self.backtrack
				if(len(self.movesStack) == 0):
					return ("done", (0,0), 0, 0)
				else:
					coordinates = self.movesStack.pop()

				valueIn = 1
				return ("input", coordinates, valueIn, 1.0)

                #return ("done", (0,0), 0, 0)
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
