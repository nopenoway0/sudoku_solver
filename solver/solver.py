import solverclass as sc
import sudoku_creater as creator
#
# Create agent, and sudoku puzzle and apply it to environment. Need to get sudoku from sudoku_creator. Not implemented
#

puzzle = creator.Sudoku()
puzzle.generate()
puzzle.hide_solution()

agent = sc.SAgent(sc.BruteAlgorithm(puzzle))
env = sc.SEnvironment(agent, puzzle)
print(env.puzzle)
env.step()
print(agent.algorithm.num_map[0][4])
