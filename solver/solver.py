import solverclass as sc
import sudoku_creater as creator
import time
#
# Create agent, and sudoku puzzle and apply it to environment. Need to get sudoku from sudoku_creator. Not implemented
#

puzzle = creator.Sudoku()
puzzle.generate()
puzzle.hide_solution()

agent = sc.SAgent(sc.BruteAlgorithm(puzzle))
env = sc.SEnvironment(agent, puzzle)
print(env.puzzle)
for x in range(0,9):
	env.step()
	print(env.puzzle)
	time.sleep(0.2)
print(env.puzzle.submit())