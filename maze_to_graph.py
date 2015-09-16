import collections
import Graph
from collections import deque

height=0
width=0

def process_maze(file):
    maze = open(file, "r")
    line = maze.readline()

    line_num = 0
    maze_array = []

    while line != "":
        text_to_nodes(line, line_num, maze_array)
        line = maze.readline()
        line_num += 1
    global height
    height =line_num
    print(height)
    return maze_array
#testtest
def text_to_nodes(text, num, arr):
    arr.append([])
    y=0
    for x in text:
        if(x != '\n'):
            y=y+1
            arr[num].append(x)
    global width
    width=y



def find_pacman(arr):
    pacman = collections.namedtuple('Pacman', ['h', 'w'])
    for x in range(0, height):
        for y in range(0, width):
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

def bfs_maze(maze, p_x, p_y):
    pathNodes=[]
    for x in range(0, height):
        pathNodes.append([])
        for y in range(0, width):
            if(maze[x][y]=='%'):
                pathNodes[x].append('%')
            else:
                pathNodes[x].append('0')
    counter=0
    visitedNode=[]
    for x in range(0, height):
        visitedNode.append([])
        for y in range(0, width):
            visitedNode[x].append('0')
    #print_maze_array(visitedNode)
    tuple=(p_y,p_x, '$')
    node=tuple
    queue=deque((tuple, ))

    while(len(queue) > 0):
        node=queue.pop()
        #print(node)
        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] ='1'
            if maze[node[0]][node[1]] == 'P':
                pathNodes[node[0]][node[1]] ='P'
            pathNodes[node[0]][node[1]] ='.'
            #pathNodes[node[0]][node[1]] =node[2]
            counter=counter+1
            if maze[node[0]][node[1]] == '.':
                pathNodes[node[0]][node[1]] ='.'
                print_maze_array(pathNodes)
                return (True, node[0], node[1])

            for n in adjacentNodes(maze, node):
                if visitedNode[n[0]][n[1]] == '0':
                    queue.appendleft(n)
    print_maze_array(pathNodes)
    return (False, node[0], node[1])


def adjacentNodes(maze, node):
    retList=[]

    if maze[node[0]+1][node[1]] != '%': #down
        #print(1)
        #print('upcheck=: '+str(node[0]+1)+' '+str(node[1])+' : '+maze[node[0]+1][node[1]])
        retList.append((node[0]+1,node[1], '!'))
    if maze[node[0]-1][node[1]] != '%': #up
        #print(2)
        retList.append((node[0]-1,node[1], '^'))
    if maze[node[0]][node[1]-1] != '%': #left
        retList.append((node[0],node[1]-1, '<'))
        #print(3)
    if maze[node[0]][node[1]+1] != '%': #right
        #print(4)
        retList.append((node[0],node[1]+1, '>'))
    #print(retList)
    return retList


def dfs_maze(maze, p_x, p_y):
    pathNodes=[]
    for x in range(0, height):
        pathNodes.append([])
        for y in range(0, width):
            if(maze[x][y]=='%'):
                pathNodes[x].append('%')
            else:
                pathNodes[x].append('0')
    counter=0
    visitedNode=[]
    for x in range(0, height):
        visitedNode.append([])
        for y in range(0, width):
            visitedNode[x].append('0')
    #print_maze_array(visitedNode)
    tuple=(p_y,p_x, '$')
    node=tuple
    stack=[node]

    while(len(stack) > 0):
        node=stack.pop()
        #print(node)
        if visitedNode[node[0]][node[1]] == '0':
            visitedNode[node[0]][node[1]] ='1'
            if maze[node[0]][node[1]] == 'P':
                pathNodes[node[0]][node[1]] ='P'
            pathNodes[node[0]][node[1]] ='.'
            #pathNodes[node[0]][node[1]] =node[2]
            counter=counter+1
            if maze[node[0]][node[1]] == '.':
                pathNodes[node[0]][node[1]] ='.'
                print_maze_array(pathNodes)
                return (True, node[0], node[1])

            for n in adjacentNodes(maze, node):
                if visitedNode[n[0]][n[1]] == '0':
                    stack.append(n)
    print_maze_array(pathNodes)
    return (False, node[0], node[1])








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
#print(m[36][35])
#bfs_maze(m, p.w, p.h)
print(width)
print(height)
print(p.h)
print(p.w)
print(dfs_maze(m, p.w, p.h))
print(bfs_maze(m, p.w, p.h))
