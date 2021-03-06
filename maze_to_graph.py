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

def find_ghost(arr):
    ghost_list = []

    for x in range(0, maze_height):
        for y in range(0, maze_width):
            if(arr[x][y] == "G"):
                g = [x, y, 'right']
                ghost_list.append(g)
    return ghost_list

def find_spirit(arr):
    ghost_list = []

    for x in range(0, maze_height):
        for y in range(0, maze_width):
            if(arr[x][y] == "S"):
                g = [x, y, 'up']
                ghost_list.append(g)
    return ghost_list


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



def maze_copy(path_nodes, maze):
    for x in range(0, maze_height):
        path_nodes.append([])
        for y in range(0, maze_width):
            path_nodes[x].append(maze[x][y])



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

def heuristic_cost_estimate(p_y, p_x, g_y, g_x, method, turn_cost, forward_cost, dir):

    if(method == "MANHATTAN"):
        distance = abs(p_y - g_y) + abs(p_x - g_x)
        return distance
    elif(method == "CHICAGO"): #heuristic when diagonals are allowed
        dx = 2*abs(p_x - g_x)
        dy = abs(p_y - g_y)
        diagonalCost = sqrt(2)
        return ((dx + dy) + (diagonalCost - 2) * min(dx, dy))
    elif(method == "SANFRAN"): #heuristic when the turn and forward costs differ
        distance = abs(p_y - g_y) + abs(p_x - g_x)
        if(dir == "TURN"):
            distance *= turn_cost
        else:
            distance *= forward_cost
        return distance

    else:
        return -1

def a_star(maze, p_x, p_y, g_x, g_y, forward_cost, turn_cost, h):

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
                move_cost = checkCostOfTurning(n[3], node[3], turn_cost, forward_cost)
                new_cost += move_cost

                move_type = "TURN"
                if(move_cost == forward_cost):
                    move_type = "FORWARD"

                if (n not in cost_so_far or new_cost < cost_so_far[n]) and visitedNode[n[0]][n[1]] == '0':
                    cost_so_far[n] = new_cost
                    priority = new_cost + heuristic_cost_estimate(n[0], n[1], g_y, g_x, h, turn_cost, forward_cost, move_type)
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

def a_star_ghost(maze, p_x, p_y, g_x, g_y, forward_cost, turn_cost, h, ghost_arr, spirit_arr):

    nodes_expanded = 0
    path_cost = 0
    found = False

    came_from = {}
    cost_so_far = {}

    path_nodes = []
    maze_to_array(path_nodes, maze)

    ghost_maze=[]
    maze_copy(ghost_maze, maze)
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

    dir='right'
    while(len(queue) > 0):
        node = heappop(queue)[1]

        for spirit in spirit_arr:
            spirit_y = spirit[0]
            spirit_x = spirit[1]
            dir = spirit[2]

            if(dir=='up'):
                if(ghost_maze[spirit_y - 1][spirit_x] == '%'):
                        spirit[0] = spirit_y + 1
                        spirit[2] = 'down'
                else:
                       spirit[0] = spirit_y - 1
            elif(dir=='down'):
                if(ghost_maze[spirit_y + 1][spirit_x] == '%'):
                        spirit[0] = spirit_y - 1
                        spirit[2] = 'up'
                else:
                        spirit[0] = spirit_y + 1

            if(node[0] == spirit_y and node[1] == spirit_x):
                node = heappop(queue)[1]

            path_nodes[spirit[0]][spirit[1]] = "s"

        for ghost in ghost_arr:
            ghost_y = ghost[0]
            ghost_x = ghost[1]
            dir = ghost[2]

            if(dir=='right'):
                if(ghost_maze[ghost_y][ghost_x+1] == '%'):
                        ghost[1] = ghost_x -1
                        ghost[2] = 'left'
                else:
                       ghost[1] = ghost_x +1
            elif(dir=='left'):
                if(ghost_maze[ghost_y][ghost_x-1] == '%'):
                        ghost[1] = ghost_x +1
                        ghost[2] = 'right'
                else:
                        ghost[1] = ghost_x -1

            if(node[0] == ghost_y and node[1] == ghost_x):
                node = heappop(queue)[1]

            path_nodes[ghost[0]][ghost[1]] = "g"

        if ghost_maze[node[0]][node[1]] == '.' and visitedNode[node[0]][node[1]] == '0':
                path_cost += checkCostOfTurning(node[3], came_from[node][3], turn_cost, forward_cost)
                path_nodes[node[0]][node[1]] = "."
                path_nodes[p_y][p_x] = "P"
                goal = node
                found = True
                break

        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] = '1'

            nodes_expanded += 1

            for n in adjacentNodesAStar(ghost_maze, node):

                new_cost = cost_so_far[node]
                new_cost += checkCostOfTurning(n[3], node[3], turn_cost, forward_cost)

                if (n not in cost_so_far or new_cost < cost_so_far[n]) and visitedNode[n[0]][n[1]] == '0':
                    cost_so_far[n] = new_cost
                    priority = new_cost + heuristic_cost_estimate(n[0], n[1], g_y, g_x, h, turn_cost, forward_cost, "")
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
    path_cost = 0

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
                    priority = new_cost + heuristic_cost_estimate(p_y, p_x, g_y, g_x, h, 1, 1, "")
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
    ghost_pacman = find_ghost(m)

    if(method == "BFS"):
        result = bfs_maze(m, p.w, p.h)
        print("Nodes expanded: " + str(result[1]))
        print("Path cost: " + str(result[2]))
        print("")
        return True
    elif(method == "DFS"):
        result = dfs_maze(m, p.w, p.h)
        print("Nodes expanded: " + str(result[1]))
        print("Path cost: " + str(result[2]))
        print("")
        return True
    elif(method == "GREEDY"):
        result = greedy_bfs_maze(m, p.w, p.h, g.w, g.h)
        print("Nodes expanded: " + str(result[1]))
        print("Path cost: " + str(result[2]))
        print("")
        return True
    elif(method == "A*"):
        result = a_star(m, p.w, p.h, g.w, g.h, forward_cost, turn_cost, h)
        print("Nodes expanded: " + str(result[1]))
        print("Path cost: " + str(result[2]))
        print("")
        return True
    elif(method == "A*_ghost"):
        ghost_array = find_ghost(m)
        spirit_array = find_spirit(m)
        result = a_star_ghost(m, p.w, p.h, g.w, g.h, forward_cost, turn_cost, h, ghost_array, spirit_array)
        print("Nodes expanded: " + str(result[1]))
        print("Path cost: " + str(result[2]))
        print("")
        return True
    elif(method == "A*_Diagonal"):
        result = a_star_diagonal(m, p.w, p.h, g.w, g.h, h)
        print("Nodes expanded: " + str(result[1]))
        print("Path cost: " + str(result[2]))
        print("")
        return True
    else:
        return False

#Run program
'''solve("bigMaze.txt", "BFS", 1, 1, "MANHATTAN")
solve("bigMaze.txt", "DFS", 1, 1, "MANHATTAN")
solve("bigMaze.txt", "GREEDY", 1, 1, "MANHATTAN")
solve("bigMaze.txt", "A*", 1, 1, "MANHATTAN")
solve("mediumMaze.txt", "BFS", 1, 1, "MANHATTAN")
solve("mediumMaze.txt", "DFS", 1, 1, "MANHATTAN")
solve("mediumMaze.txt", "GREEDY", 1, 1, "MANHATTAN")
solve("mediumMaze.txt", "A*", 1, 1, "MANHATTAN")
solve("openMaze.txt", "BFS", 1, 1, "MANHATTAN")
solve("openMaze.txt", "DFS", 1, 1, "MANHATTAN")
solve("openMaze.txt", "GREEDY", 1, 1, "MANHATTAN")
solve("openMaze.txt", "A*", 1, 1, "MANHATTAN")

solve("smallTurns.txt", "A*", 2, 1, "MANHATTAN")
solve("smallTurns.txt", "A*", 2, 1, "SANFRAN")

solve("smallTurns.txt", "A*", 1, 2, "MANHATTAN")
solve("smallTurns.txt", "A*", 1, 2, "SANFRAN")

solve("bigTurns.txt", "A*", 2, 1, "MANHATTAN")
solve("bigTurns.txt", "A*", 2, 1, "SANFRAN")

solve("bigTurns.txt", "A*", 1, 2, "MANHATTAN")
solve("bigTurns.txt", "A*", 1, 2, "SANFRAN")
'''
'''
solve("smallGhost.txt", "A*", 1, 1, "MANHATTAN")
solve("smallGhost.txt", "A*_ghost", 1, 1, "MANHATTAN")
solve("mediumGhost.txt", "A*", 1, 1, "MANHATTAN")
solve("mediumGhost.txt", "A*_ghost", 1, 1, "MANHATTAN")
solve("bigGhost.txt", "A*", 1, 1, "MANHATTAN")
solve("bigGhost.txt", "A*_ghost", 1, 1, "MANHATTAN")

solve("smallMultiGhost.txt", "A*", 1, 1, "MANHATTAN")
solve("smallMultiGhost.txt", "A*_ghost", 1, 1, "MANHATTAN")

solve("mediumMultiGhost.txt", "A*", 1, 1, "MANHATTAN")
solve("mediumMultiGhost.txt", "A*_ghost", 1, 1, "MANHATTAN")

solve("bigMultiGhost.txt", "A*", 1, 1, "MANHATTAN")
solve("bigMultiGhost.txt", "A*_ghost", 1, 1, "MANHATTAN")'''


solve("openMaze.txt", "A*", 1, 1, "MANHATTAN")
solve("openMaze.txt", "A*_Diagonal", 1, 1, "CHICAGO")

solve("mediumMaze.txt", "A*", 1, 1, "MANHATTAN")
solve("mediumMaze.txt", "A*_Diagonal", 1, 1, "CHICAGO")