import borrowed as pc
import time
import threading
__author__ = 'Ripley6811'
__contact__ = 'python at boun.cr'
__copyright__ = ''
__license__ = ''
__date__ = 'Thu Aug 30 10:09:06 2012'
__version__ = '0.1'
print "###########################################################################"
print "Uses JWJ sudoku generator available at: http://code.activestate.com/recipes/578250-sudoku-game-generator/"
print "###########################################################################"

finished = False
num_threads = 4
total_puzzles = 100 
file_lock = threading.Lock()
puzzle_number = 1
print_lock = threading.Lock()

def alive(name):
	while(finished == False):
		with print_lock:
			print ".",
		time.sleep(0.5)

def create_puzzles(name, count, file):
	global puzzle_number
	for x in range(0,count):
		puzzle = pc.main()
		with file_lock:
			file.write(str(puzzle[0]))
			file.write("\n\n")
			file.write(str(puzzle[1]))
			file.write("\n\n")
			with print_lock:
				print ("\npuzzle %d finished\n" % (puzzle_number))
				puzzle_number += 1

raw_input("Uses 4 threads to create 100 different puzzles\nPress any key to begin...")
start = time.time()
puzzles_per_thread = total_puzzles / num_threads
save_puzzles = open("puzzles", 'w')
t1 = threading.Thread(target = alive, args = ("Printer",))
puz_threads = []

for count in range(0, num_threads):
	puz_threads.append(threading.Thread(target = create_puzzles, args = ("creator %d" % (count),puzzles_per_thread, save_puzzles)))
try:
	t1.start()
	for threads in puz_threads:
		threads.start()
except:
	print "Error"

for threads in puz_threads:
	threads.join()
finished = True
save_puzzles.close()
t1.join()
end = time.time()
print("Finished in %ds" % (end - start))
