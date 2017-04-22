import solverclass as sc
import sudoku_creater as creator
import time
import os
#
# Create agent, and sudoku puzzle and apply it to environment. Need to get sudoku from sudoku_creator. Not implemented
#
#test puzzle creation

points = ((0,2,9), (0,3,2), (0,6,6), (1,0,5), (1,1,1), (1,2,8), (1,5,4), (2,4,3), (2,8,5), (3,1,2), (3,2,7), (3,5,5), (3,8,8), (4,1,8), (4,2,5), (4,4,1), (4,6,9), (4,7,4), (5,0,1), (5,3,6), (5,6,5), (5,7,2)
	, (7,3,5), (7,6,4), (7,7,3), (7,8,9) , (6,0,4), (6,4,9), (8,2,3), (8,5,6), (8,6,7))

puzzle_amount = 1

step_count = 50

puzzle = creator.Sudoku(points)

agent = sc.SAgent(sc.NakedCandidateAlgorithm(puzzle))
env = sc.SEnvironment(agent, puzzle)
print(env.puzzle)
total_correct = 0
start = time.time()
for z in range(0, puzzle_amount):
	puzzle.generate(points)
	#puzzle.hide_solution()
	raw_input(puzzle)
	agent = sc.SAgent(sc.NakedCandidateAlgorithm(puzzle))
	env = sc.SEnvironment(agent, puzzle)
	for x in range(0, step_count):
		os.system("clear")
		if(env.step()):
			break
		#print(agent.algorithm.print_nm_map())
		print(env.puzzle)
		#time.sleep(1)
		#raw_input()
	agent.algorithm.crosshatch()
	agent.algorithm.print_nm_map()
	print(env.puzzle)
	#print(env.puzzle.get_solution())
	#print(agent.actions)
	# Print accuracy (number rights, total number)
	correct, solution = env.puzzle.submit()
	total_correct += correct
#end = time.time()
#print("Percentage correct = %.2f%% across %d puzzles with runtime: %.2fs with average of %.2fs per puzzle" % ((total_correct / (puzzle.obfus*puzzle_amount*1.0)) *100, puzzle_amount, end - start, (end-start) / puzzle_amount))