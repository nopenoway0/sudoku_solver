import solverclass as sc
import sudoku_creater as creator
import time
import os
import importer as imp

#load puzzle list from text file
puzzle_list = imp.load()
# Create agent, and sudoku puzzle and apply it to environment. Need to get sudoku from sudoku_creator. Not implemented
#
# sample hard puzzle
#points = ((0,2,9), (0,3,2), (0,6,6), (1,0,5), (1,1,1), (1,2,8), (1,5,4), (2,4,3), (2,8,5), (3,1,2), (3,2,7), (3,5,5), (3,8,8), (4,1,8), (4,2,5), (4,4,1), (4,6,9), (4,7,4), (5,0,1), (5,3,6), (5,6,5), (5,7,2)
#	, (7,3,5), (7,6,4), (7,7,3), (7,8,9) , (6,0,4), (6,4,9), (8,2,3), (8,5,6), (8,6,7))

puzzle_amount = 1

# Max amount of actions
step_count = 100
puzzle = creator.Sudoku()
agent = sc.SAgent(sc.NakedCandidateAlgorithm(puzzle))
env = sc.SEnvironment(agent, puzzle)
percentage = 0
puzzles_solved = 0
candidate_score = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
start = time.time()

#need to add loop to call backtrack then bens algo again.
#keep checking until solved
for z in range(0, len(puzzle_list)):
	if(z % 2 == 0):
		pass
	else:
		puzzle = puzzle_list[z]
		#raw_input(puzzle)
		agent = sc.SAgent(sc.NakedCandidateAlgorithm(puzzle))
		env = sc.SEnvironment(agent, puzzle)
		for x in range(0, step_count):
			#os.system("clear")
			if(env.step()):
				break
			print(env.puzzle)
			print("Current percentage: %.2f" % (percentage))
			#time.sleep(1)
        	#time.sleep(0.01)
	        agent.algorithm.crosshatch()
	    	#print(env.puzzle)

		percentage += creator.Sudoku.compare_with_solution(puzzle, puzzle_list[z - 1]) / 81.0
		if(creator.Sudoku.compare_with_solution(puzzle, puzzle_list[z - 1])/ 81.0 == 1.0):
		    puzzles_solved += 1
        #else:
			#print(env.puzzle)
			#print(puzzle_list[z-1])
        #if(creator.Sudoku.compare_with_solution(puzzle, puzzle_list[z - 1])/ 81.0 < 1.0):
		#	raw_input("imperfect score on puzzle: " + str(z) + " perc " + str(creator.Sudoku.compare_with_solution(puzzle, puzzle_list[z - 1])/ 81.0))
end = time.time()
print("Time taken to solve %d puzzles: %.2fs\nCorrect percentage %.2f\nPercentage of puzzles solved %d/%s" % (len(puzzle_list) / 2, end - start, percentage, puzzles_solved, len(puzzle_list) / 2))
