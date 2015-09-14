import collections
import Graph

def process_maze(file):
    maze = open(file, "r")
    line = maze.readline()

    line_num = 0
    maze_array = []

    while line != "":
        text_to_nodes(line, line_num, maze_array)
        line = maze.readline()
        line_num += 1

    return maze_array
#testtest
def text_to_nodes(text, num, arr):
    arr.append([])
    for x in text:
        arr[num].append(x)

def find_pacman(arr):
    pacman = collections.namedtuple('Pacman', ['x', 'y'])
    for i in arr:
        for j in arr:
            if(j == "P"):
                p = pacman(i, j)
                return p
    p = pacman(-1, -1)
    return p

def print_maze_array(arr):
    for i in arr:
        print(i)

def bfs_maze_solution(maze, p_x, p_y):
    maze_sln = maze

    q = []
    g = Graph.Graph()

    start = Graph.Node()
    start.distance = 0

    g.nodes.append(start)
    q.insert(0, start)

    while(q != []):
        curr = q.pop()
        if(curr == "."):
            break

        check_node(p_x + 1, p_y, curr, maze_sln, q)
        check_node(p_x, p_y - 1, curr, maze_sln, q)
        check_node(p_x, p_y + 1, curr, maze_sln, q)
        check_node(p_x - 1, p_y, curr, maze_sln, q)

def check_node(x, y, node, maze, q):
    n = maze[x][y] #need to look up NODE structure
    if(n != "%" & n.distance == 1000000):
        n.distance = node.distance + 1
        n.parent = node
        q.insert(n, 0)




#Run program
m = process_maze("Maze/bigMaze.txt")
p = find_pacman(m)
#bfs_maze_solution(m, p.x, p.y)
print_maze_array(m)