import re
import sudoku_creater as sc
def load(file_name="puzzles"):
	with open(file_name) as file:
		text = file.readlines()
	text = str(text)
	tokens = re.split("[^0-9]+", text)
	tokens = tokens[1:len(tokens) - 1]
	count = 0
	puzzle_list = []
	coordinate_list = []
	for num in tokens:
		if(int(num) == 0):
			coordinate_list.append((count/9, count%9, -1))
		else:
			coordinate_list.append((count/9, count%9, int(num)))
		count = count + 1
		if(count % 81 == 0):
			count = 0
			puzzle_list.append(sc.Sudoku(tuple(coordinate_list)))
			coordinate_list = []
	return puzzle_list