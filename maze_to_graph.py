import collections
from collections import deque

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
    temp='';
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

def bfs_maze(maze, p_x, p_y):

    path_nodes = []
    maze_to_array(path_nodes, maze)

    counter=0
    visitedNode=[]
    for x in range(0, maze_height):
        visitedNode.append([])
        for y in range(0, maze_width):
            visitedNode[x].append('0')

    tuple = (p_y, p_x,'$')
    node = tuple
    queue = deque((tuple, ))

    while(len(queue) > 0):
        node = queue.pop()
        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] ='1'
            if maze[node[0]][node[1]] == 'P':
                path_nodes[node[0]][node[1]] ='P'
            else:
                path_nodes[node[0]][node[1]] ='.'

            counter += 1

            if maze[node[0]][node[1]] == '.':
                path_nodes[node[0]][node[1]] ='.'
                print_maze_array(path_nodes)
                return (True, node[0], node[1])

            for n in adjacentNodes(maze, node):
                if visitedNode[n[0]][n[1]] == '0':
                    queue.appendleft(n)

    print_maze_array(path_nodes)
    return (False, node[0], node[1])

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


def dfs_maze(maze, p_x, p_y):
    path_nodes=[]
    maze_to_array(path_nodes, maze)

    counter=0
    visitedNode=[]

    for x in range(0, maze_height):
        visitedNode.append([])
        for y in range(0, maze_width):
            visitedNode[x].append('0')

    tuple = (p_y,p_x, '$')
    node = tuple
    stack = [node]

    while(len(stack) > 0):
        node = stack.pop()
        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] ='1'
            if maze[node[0]][node[1]] == 'P':
                path_nodes[node[0]][node[1]] ='P'
            else:
                path_nodes[node[0]][node[1]] ='.'

            counter += 1

            if maze[node[0]][node[1]] == '.':
                path_nodes[node[0]][node[1]] ='.'
                print_maze_array(path_nodes)
                return (True, node[0], node[1])

            for n in adjacentNodes(maze, node):
                if visitedNode[n[0]][n[1]] == '0':
                    stack.append(n)

    print_maze_array(path_nodes)
    return (False, node[0], node[1])

#Run program
m = process_maze("Maze/bigMaze.txt")
p = find_pacman(m)
#print_maze_array(m)
#print(maze_width)
#print(maze_height)
#print(p.h)
#print(p.w)
#print(dfs_maze(m, p.w, p.h))
#print(bfs_maze(m, p.w, p.h))
