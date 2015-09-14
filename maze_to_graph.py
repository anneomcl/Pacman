
def process_maze(file):
    maze = open(file, "r")
    line = maze.readline()

    line_num = 0
    maze_array = []

    while line != "":
        text_to_nodes(line, line_num, maze_array)
        line = maze.readline()
        line_num += 1

    print_maze_array(maze_array)

def print_maze_array(arr):
    for i in arr:
        print(i)

def text_to_nodes(text, num, arr):
    arr.append([])
    for x in text:
        arr[num].append(x)

process_maze("Maze/bigMaze.txt")