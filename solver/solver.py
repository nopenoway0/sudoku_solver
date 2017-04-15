import solverclass as sc
import sudoku_creater as creator
import time
import os
#
# Create agent, and sudoku puzzle and apply it to environment. Need to get sudoku from sudoku_creator. Not implemented
#

puzzle_amount = 1

step_count = 50

puzzle = creator.Sudoku()
puzzle.generate()
puzzle.hide_solution()

agent = sc.SAgent(sc.NakedCandidateAlgorithm(puzzle))
env = sc.SEnvironment(agent, puzzle)
print(env.puzzle)
total_correct = 0
start = time.time()
for z in range(0, puzzle_amount):
	puzzle = creator.Sudoku()
	puzzle.generate()
	puzzle.hide_solution()

	agent = sc.SAgent(sc.NakedCandidateAlgorithm(puzzle))
	env = sc.SEnvironment(agent, puzzle)
	for x in range(0, step_count):
		os.system("clear")
		if(env.step()):
			break
		#print(env.puzzle)
		#time.sleep(0.1)

	#print(env.puzzle)
	#print(env.puzzle.get_solution())
	# Print accuracy (number rights, total number)
	(correct, solution) = env.puzzle.submit()
	total_correct += correct
end = time.time()
print("Percentage correct = %.2f%% across %d puzzles with runtime: %.2fs with average of %.2fs per puzzle" % ((total_correct / (54.0*puzzle_amount)) *100, puzzle_amount, end - start, (end-start) / puzzle_amount))