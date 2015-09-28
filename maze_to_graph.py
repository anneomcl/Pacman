import collections
from collections import deque
from heapq import heappush, heappop
from math import sqrt

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

def adjacentNodes2(maze, node):
    retList=[]

    if maze[node[0]+1][node[1]] != '%': #down
        retList.append((node[0]+1,node[1], '!'))
    if maze[node[0]-1][node[1]] != '%': #up
        retList.append((node[0]-1,node[1], '^'))
    if maze[node[0]][node[1]-1] != '%': #left
        retList.append((node[0],node[1]-1, '<'))
    if maze[node[0]][node[1]+1] != '%': #right
        retList.append((node[0],node[1]+1, '>'))

    if maze[node[0]-1][node[1]-1] != '%': #upLeft
        retList.append((node[0]-1,node[1]-1, 'UL'))
    if maze[node[0]-1][node[1]+1] != '%': #upRight
        retList.append((node[0]-1,node[1]+1, 'UR'))
    if maze[node[0]+1][node[1]-1] != '%': #downLeft
        retList.append((node[0]+1,node[1]-1, 'DL'))
    if maze[node[0]+1][node[1]+1] != '%': #downRight
        retList.append((node[0]+1,node[1]+1, 'DR'))
    return retList

def bfs_maze(maze, p_x, p_y):
    nodes_expanded = 0
    path_cost = 0

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
    path_cost = 0
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

def greedy_bfs_maze(maze, p_x, p_y, g_x, g_y):
    path_cost = 0
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

        if maze[node[0]][node[1]] == '.' and visitedNode[node[0]][node[1]] == '0':
                path_cost += 1
                path_nodes[p_y][p_x] = "P"
                print_maze_array(path_nodes)
                print("GREEDY BFS")
                return (True, nodes_expanded, path_cost)

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

def heuristic_cost_estimate(p_y, p_x, g_y, g_x, method):

    if(method == "MANHATTAN"):
        distance = abs(p_y - g_y) + abs(p_x - g_x)
        return distance
    elif(method == "CHICAGO"):
        dx = abs(p_x - g_x)
        dy = abs(p_y - g_y)
        diagonalCost = sqrt(2)
        return ((dx + dy) + (diagonalCost - 2) * min(dx, dy))
    else:
        return -1

def a_star(maze, p_x, p_y, g_x, g_y):

    nodes_expanded = 0
    path_cost = 0
    found = False

    came_from = {}
    cost_so_far = {}

    path_nodes = []
    maze_to_array(path_nodes, maze)

    goal = ()

    visitedNode=[]
    for x in range(0, maze_height):
        visitedNode.append([])
        for y in range(0, maze_width):
            visitedNode[x].append('0')

    t = (0, (p_y, p_x,'$', "RIGHT"))
    queue = []
    heappush(queue, t)

    came_from[t[1]] = None
    cost_so_far[t[1]] = 0

    while(len(queue) > 0):
        node = heappop(queue)[1]

        if maze[node[0]][node[1]] == '.' and visitedNode[node[0]][node[1]] == '0':
                path_cost += checkCostOfTurning(node[3], came_from[node][3], turn_cost, forward_cost)
                path_nodes[node[0]][node[1]] = "."
                path_nodes[p_y][p_x] = "P"
                goal = node
                found = True
                break

        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] = '1'

            nodes_expanded += 1

            for n in adjacentNodesAStar(maze, node):

                new_cost = cost_so_far[node]
                new_cost += checkCostOfTurning(n[3], node[3], turn_cost, forward_cost)

                if (n not in cost_so_far or new_cost < cost_so_far[n]) and visitedNode[n[0]][n[1]] == '0':
                    cost_so_far[n] = new_cost
                    priority = new_cost + heuristic_cost_estimate(n[0], n[1], g_y, g_x, h)
                    heappush(queue, (priority, (n[0], n[1], n[2], n[3])))
                    came_from[n] = node

    curr = came_from[goal]
    del came_from[goal]
    while(len(came_from) > 0):
        if(curr[2] != '$'):
            path_cost += checkCostOfTurning(curr[3], came_from[curr][3], turn_cost, forward_cost)
            path_nodes[curr[0]][curr[1]] = '.'
            temp = curr
            curr = came_from[temp]
            del came_from[temp]
        else:
            break

    print_maze_array(path_nodes)
    print("A*")
    return (found, nodes_expanded, path_cost)

def checkCostOfTurning(a, b, turn_cost, forward_cost):

    cost = 0

    if a == b:
        cost += forward_cost
    elif (a == "RIGHT" or a == "LEFT") and (b == "UP" or b == "DOWN"):
        cost += turn_cost
    elif (b == "RIGHT" or b == "LEFT") and (a == "UP" or a == "DOWN"):
        cost += turn_cost
    else:
        cost += turn_cost*2

    return cost

def adjacentNodesAStar(maze, node):
    retList=[]

    if maze[node[0]+1][node[1]] != '%': #down
        retList.append((node[0]+1,node[1], '!', "DOWN"))
    if maze[node[0]-1][node[1]] != '%': #up
        retList.append((node[0]-1,node[1], '^', "UP"))
    if maze[node[0]][node[1]-1] != '%': #left
        retList.append((node[0],node[1]-1, '<', "LEFT"))
    if maze[node[0]][node[1]+1] != '%': #right
        retList.append((node[0],node[1]+1, '>', "RIGHT"))
    return retList

def a_star_diagonal(maze, p_x, p_y, g_x, g_y, h):

    nodes_expanded = 0
    path_cost = 1

    came_from = {}
    cost_so_far = {}

    path_nodes = []
    maze_to_array(path_nodes, maze)

    goal = ()

    #closed set
    visitedNode=[]
    for x in range(0, maze_height):
        visitedNode.append([])
        for y in range(0, maze_width):
            visitedNode[x].append('0')

    #frontier
    #node: y, x, symbol, f score, g score
    t = (0, (p_y, p_x,'$'))
    queue = []
    heappush(queue, t)

    found = False

    came_from[t[1]] = None
    cost_so_far[t[1]] = 0

    while(len(queue) > 0):
        node = heappop(queue)[1]

        if maze[node[0]][node[1]] == '.' and visitedNode[node[0]][node[1]] == '0':
                path_cost += 1
                path_nodes[node[0]][node[1]] = "."
                path_nodes[p_y][p_x] = "P"
                goal = node
                found = True
                break

        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] = '1'

            nodes_expanded += 1

            for n in adjacentNodes2(maze, node):
                if(n[2]=='UR' or n[2]=='UL' or n[2]=='DR' or n[2]=='DL'):
                    new_cost = cost_so_far[node] + sqrt(2)
                else:
                    new_cost = cost_so_far[node] + 1
                if (n not in cost_so_far or new_cost < cost_so_far[n]) and visitedNode[n[0]][n[1]] == '0':
                    cost_so_far[n] = new_cost
                    priority = new_cost + heuristic_cost_estimate(p_y, p_x, g_y, g_x, h)
                    heappush(queue, (priority, (n[0], n[1], n[2])))
                    came_from[n] = node

    curr = came_from[goal]
    del came_from[goal]
    while(len(came_from) > 0):
        if(curr[2] != '$'):
            path_cost += 1
            path_nodes[curr[0]][curr[1]] = '.'
            temp = curr
            curr = came_from[temp]
            del came_from[temp]
        else:
            break

    print_maze_array(path_nodes)
    print("A*")
    return (found, nodes_expanded, path_cost)

def solve(file, method, forward_cost, turn_cost, h):
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
        print(a_star(m, p.w, p.h, g.w, g.h, forward_cost, turn_cost, h))
        return True
    elif(method == "A*_Diagonal"):
        print(a_star_diagonal(m, p.w, p.h, g.w, g.h, h))
        return True
    else:
        return False

#Run program
#solve("bigMaze.txt", "BFS")
#solve("bigMaze.txt", "DFS")
#solve("bigMaze.txt", "GREEDY")
#solve("bigMaze.txt", "A*")
#solve("mediumMaze.txt", "BFS")
#solve("mediumMaze.txt", "DFS")
#solve("mediumMaze.txt", "GREEDY")
#solve("mediumMaze.txt", "A*")
#solve("openMaze.txt", "BFS")
#solve("openMaze.txt", "DFS")
#solve("openMaze.txt", "GREEDY")
#solve("openMaze.txt", "A*")
solve("bigMaze.txt", "A*", 1, 1, "MANHATTAN")
solve("bigMaze.txt", "A*", 1, 2, "MANHATTAN")
solve("bigMaze.txt", "A*", 2, 1, "MANHATTAN")
solve("openMaze.txt", "A*", "MANHATTAN")
solve("openMaze.txt", "A*_Diagonal", "CHICAGO")