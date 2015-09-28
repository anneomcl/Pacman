import collections
from collections import deque
from heapq import heappush, heappop

maze_height = 0
maze_width = 0

def process_maze(file):
    maze = open(file, "r")
    line = maze.readline()

    line_num = 0
    maze_array = []

    while line != "":
        text_to_nodes(line, line_num, maze_array)
        line = maze.readline()
        line_num += 1
    global maze_height
    maze_height = line_num
    return maze_array

def text_to_nodes(text, num, arr):
    arr.append([])
    y = 0
    for x in text:
        if(x != '\n'):
            y=y+1
            arr[num].append(x)
    global maze_width
    maze_width = y

def find_pacman(arr):
    pacman = collections.namedtuple('Pacman', ['h', 'w'])
    for x in range(0, maze_height):
        for y in range(0, maze_width):
            if(arr[x][y] == "P"):
                p = pacman(x, y)
                return p
    p = pacman(-1, -1)
    return p

def print_maze_array(arr):
    temp=''
    for i in arr:
        for x in i:
            temp=temp+x
        print(temp+'\n', end='')
        temp=''

def maze_to_array(path_nodes, maze):
    for x in range(0, maze_height):
        path_nodes.append([])
        for y in range(0, maze_width):
            if(maze[x][y]=='%'):
                path_nodes[x].append('%')
            else:
                path_nodes[x].append(' ')

def adjacentNodes(maze, node):
    retList=[]

    if maze[node[0]+1][node[1]] != '%': #down
        retList.append((node[0]+1,node[1], '!'))
    if maze[node[0]-1][node[1]] != '%': #up
        retList.append((node[0]-1,node[1], '^'))
    if maze[node[0]][node[1]-1] != '%': #left
        retList.append((node[0],node[1]-1, '<'))
    if maze[node[0]][node[1]+1] != '%': #right
        retList.append((node[0],node[1]+1, '>'))
    return retList

def adjacentNodesAStar(maze, node, g_y, g_x):
    retList=[]

    g_score = node[4] + 1

    if maze[node[0]+1][node[1]] != '%': #down
        f_score = g_score + heuristic_cost_estimate(node[0]+1, node[1], g_y, g_x, "MANHATTAN")
        retList.append((node[0]+1,node[1], '!', f_score, g_score))
    if maze[node[0]-1][node[1]] != '%': #up
        f_score = g_score + heuristic_cost_estimate(node[0]-1, node[1], g_y, g_x, "MANHATTAN")
        retList.append((node[0]-1,node[1], '^', f_score, g_score))
    if maze[node[0]][node[1]-1] != '%': #left
        f_score = g_score + heuristic_cost_estimate(node[0], node[1]-1, g_y, g_x, "MANHATTAN")
        retList.append((node[0],node[1]-1, '<', f_score, g_score))
    if maze[node[0]][node[1]+1] != '%': #right
        f_score = g_score + heuristic_cost_estimate(node[0], node[1]+1, g_y, g_x, "MANHATTAN")
        retList.append((node[0],node[1]+1, '>', f_score, g_score))
    return retList

def bfs_maze(maze, p_x, p_y):
    nodes_expanded = 0
    path_cost = 1

    #initializing maze to node structure
    path_nodes = []
    maze_to_array(path_nodes, maze)

    #initializing all nodes as unvisited
    visitedNode=[]
    for x in range(0, maze_height):
        visitedNode.append([])
        for y in range(0, maze_width):
            visitedNode[x].append('0')

    t = (p_y, p_x,'$')
    queue = deque((t, ))

    while(len(queue) > 0):
        node = queue.pop()
        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] ='1'
            nodes_expanded += 1

            if maze[node[0]][node[1]] == '.':
                path_cost += 1
                path_nodes[p_y][p_x] = "P"
                print_maze_array(path_nodes)
                print("BFS")
                return (True, nodes_expanded, path_cost)

            elif maze[node[0]][node[1]] != 'P':
                path_nodes[node[0]][node[1]] ='.'
                path_cost += 1

            for n in adjacentNodes(maze, node):
                if visitedNode[n[0]][n[1]] == '0':
                    queue.appendleft(n)

    path_nodes[p_y][p_x] = "P"
    print_maze_array(path_nodes)
    return (False, nodes_expanded, path_cost)

def dfs_maze(maze, p_x, p_y):
    path_cost = 1
    nodes_expanded = 0

    path_nodes=[]
    maze_to_array(path_nodes, maze)

    visitedNode=[]

    for x in range(0, maze_height):
        visitedNode.append([])
        for y in range(0, maze_width):
            visitedNode[x].append('0')

    t = (p_y,p_x, '$')
    stack = [t]

    while(len(stack) > 0):
        node = stack.pop()
        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] ='1'
            nodes_expanded += 1

            if maze[node[0]][node[1]] == '.':
                path_cost += 1
                path_nodes[p_y][p_x] = "P"
                print_maze_array(path_nodes)
                print("DFS")
                return (True, nodes_expanded, path_cost)

            elif maze[node[0]][node[1]] != 'P':
                path_nodes[node[0]][node[1]] ='.'
                path_cost += 1

            for n in adjacentNodes(maze, node):
                if visitedNode[n[0]][n[1]] == '0':
                    stack.append(n)

    print_maze_array(path_nodes)
    return (False, nodes_expanded, path_cost)

def add_by_priority(min, queue, g_y, g_x):

    stillLooking = True

    if(len(queue) < 1):
        queue.append(min)

    queueTemp = deque()
    while(len(queue) > 0):
        node = queue.pop()
        if ((abs(node[0] - g_y) + abs(node[1] - g_x)) >= (abs(min[0] - g_y) + abs(min[1] - g_x))) and stillLooking:
            queueTemp.append(min)
            queueTemp.append(node)
            stillLooking = False
        else:
            queueTemp.append(node)

    return queueTemp

def greedy_bfs_maze(maze, p_x, p_y, g_x, g_y):
    path_cost = 1
    nodes_expanded = 0

    frontier = []

    path_nodes = []
    maze_to_array(path_nodes, maze)

    visitedNode=[]
    for x in range(0, maze_height):
        visitedNode.append([])
        for y in range(0, maze_width):
            visitedNode[x].append('0')

    t = (p_y, p_x,'$')
    queue = []
    heappush(queue, t)

    while(len(queue) > 0):
        node = heappop(queue)

        path_cost += 1
        path_nodes[node[0]][node[1]] ='.'
        print_maze_array(path_nodes)
        input("Press enter")

        if maze[node[0]][node[1]] == '.' and visitedNode[node[0]][node[1]] == '0':
                path_cost += 1
                path_nodes[p_y][p_x] = "P"
                print_maze_array(path_nodes)
                print("GREEDY BFS")
                return (True, nodes_expanded, path_cost)

        if len(queue) < 1 and len(frontier) > 0:
            if(len(frontier) > 0):
                min = findMin(maze, frontier, "MANHATTAN", g_x, g_y)
                heappush(queue, min)

        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] = '1'
            nodes_expanded += 1

            for n in adjacentNodes(maze, node):
                if visitedNode[n[0]][n[1]] == '0':
                    frontier.append(n)

            if(len(frontier) > 0):
                min = findMin(maze, frontier, "MANHATTAN", g_x, g_y)
                heappush(queue, min)

    print_maze_array(path_nodes)
    return (False, nodes_expanded, path_cost)

def findMin(maze, frontier, heuristic, g_x, g_y):

    if(heuristic == "MANHATTAN"):
        min = 100000000
        best_node = (-1, -1, '')
        best_node_index = -1
        i = 0

        for node in frontier:
            distance = abs(node[0] - g_y) + abs(node[1] - g_x)
            if(distance < min):
                min = distance
                best_node = (node[0], node[1], node[2])
                best_node_index = i
            i += 1

    del frontier[best_node_index]

    return best_node

def find_goal(arr):
    goal = collections.namedtuple('Goal', ['h', 'w'])
    for x in range(0, maze_height):
        for y in range(0, maze_width):
            if(arr[x][y] == "."):
                g = goal(x, y)
                return g
    g = goal(-1, -1)
    return g

def findMinAStar(maze, frontier, heuristic, g_x, g_y):

    if(heuristic == "MANHATTAN"):
        min = 100000000
        best_node = (-1, -1, '')
        best_node_index = -1
        i = 0

        for node in frontier:
            distance = node[3] + abs(node[0] - g_y) + abs(node[1] - g_x)
            if(distance < min):
                min = distance
                best_node = (node[0], node[1], node[2], node[3])
                best_node_index = i
            i += 1

    del frontier[best_node_index]

    return best_node

def heuristic_cost_estimate(p_y, p_x, g_y, g_x, method):

    if(method == "MANHATTAN"):
        distance = abs(p_y - g_y) + abs(p_x - g_x)
        return distance
    else:
        return -1


def a_star(maze, p_x, p_y, g_x, g_y):

    nodes_expanded = 0
    path_cost = 1

    came_from = {}

    path_nodes = []
    maze_to_array(path_nodes, maze)

    #closed set
    visitedNode=[]
    for x in range(0, maze_height):
        visitedNode.append([])
        for y in range(0, maze_width):
            visitedNode[x].append('0')

    #openset
    #node: y, x, symbol, f score, g score
    t = (p_y, p_x,'$', 1000000 + heuristic_cost_estimate(p_y, p_x, g_y, g_x, "MANHATTAN"), 0)
    queue = []
    heappush(queue, t)

    while(len(queue) > 0):
        node = heappop(queue)

        if maze[node[0]][node[1]] == '.' and visitedNode[node[0]][node[1]] == '0':
                path_cost += 1
                path_nodes[p_y][p_x] = "P"
                print_maze_array(path_nodes)
                print("A*")
                return (True, nodes_expanded, path_cost)

        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] = '1'

            nodes_expanded += 1

            for n in adjacentNodesAStar(maze, node, g_y, g_x):
                if visitedNode[n[0]][n[1]] == '0':
                    tentative_g_score = node[4] + 1
                    if n not in queue or tentative_g_score < n[4]:

                        lst = list(n)
                        lst[4] = tentative_g_score
                        lst[3] = n[4] + heuristic_cost_estimate(n[0], n[1], g_y, g_x, "MANHATTAN")
                        n = tuple(lst)
                        if n not in queue:
                            heappush(queue, n)

    print_maze_array(path_nodes)
    return (False, nodes_expanded, path_cost)


def solve(file, method):
    m = process_maze("Maze/"+file)
    p = find_pacman(m)
    g = find_goal(m)

    if(method == "BFS"):
        print(bfs_maze(m, p.w, p.h))
        return True
    elif(method == "DFS"):
        print(dfs_maze(m, p.w, p.h))
        return True
    elif(method == "GREEDY"):
        print(greedy_bfs_maze(m, p.w, p.h, g.w, g.h))
        return True
    elif(method == "A*"):
        print(a_star(m, p.w, p.h, g.w, g.h))
        return True
    else:
        return False

#Run program
#solve("bigMaze.txt", "BFS")
#solve("bigMaze.txt", "DFS")
#
# solve("bigMaze.txt", "GREEDY")
#solve("bigMaze.txt", "A*")
#solve("mediumMaze.txt", "BFS")
#solve("mediumMaze.txt", "DFS")
#solve("mediumMaze.txt", "GREEDY")
#solve("mediumMaze.txt", "A*")
#solve("openMaze.txt", "BFS")
#solve("openMaze.txt", "DFS")
solve("openMaze.txt", "GREEDY")
#solve("openMaze.txt", "A*")