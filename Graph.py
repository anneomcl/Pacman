class Node:
    def __init__(self):
        self.parent = None
        self.distance = 1000000

class Graph:
    def __init__(self):
        self.nodes = []