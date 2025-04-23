from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush
from collections import deque

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)] # right / down / left / up

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    '''
    This needs to be changed, for each self.type, depending on what
    kind of data structure
    dfs = stack
    bfs = queue
    ucs = heapq
    astar = heapq
    '''
    def set_search(self):
        self.final_cost = 0
        self.grid.reset() # reset all the nodes in the path
        self.finished = False
        self.failed = False
        self.previous = {} 

        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = set() # changed it to set for better time complexity lookup
        elif self.type == "bfs":
            self.frontier = deque([self.grid.start])
            self.explored = set()
        elif self.type == "ucs":
            self.frontier = set([self.grid.start]) # since i can't change the updated new_cost, i need to make two frontier to ignore the exisiting node in the frontier
            self.frontier_heap = []
            heappush(self.frontier_heap, (0, self.grid.start))
            self.explored = set()
            self.cost_dict = {node: float('inf') for node in self.grid.nodes.keys()} # init all the distance cost to infinity
            self.cost_dict[self.grid.start] = 0 # init the cost of starting node to zero
        elif self.type == "astar":
            self.frontier = set([self.grid.start]) # since i can't change the updated new_cost, i need to make two frontier to ignore the exisiting node in the frontier
            self.frontier_heap = []
            heappush(self.frontier_heap, (0, self.grid.start))
            self.explored = set()
            self.cost_dict = {node: float('inf') for node in self.grid.nodes.keys()} # init all the distance cost to infinity
            self.cost_dict[self.grid.start] = 0 # init the cost of starting node to zero

    # This is to calculate the total cost only after we have found the path
    def get_result(self):
        total_cost = 0
        current = self.grid.goal # this is tuple[int, int]
        while not current == self.grid.start:
            if self.type == "bfs":
                total_cost += 1 
            else:
                total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    def dfs_step(self):
        if not self.frontier: # checks if frontier is empty
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()
        
        if current in self.explored: # if it is already explored
            return
        self.explored.add(current) # since we already checked if it's in explored, just push it
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        
        if current == self.grid.goal: # if we've found the goal
            self.finished = True
            return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS] # this is a list of tuple for each move
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if (not self.grid.nodes[n].puddle) and (n not in self.explored) and (n not in self.frontier):
                    self.previous[n] = current
                    if n == self.grid.goal:
                        self.explored.add(n)
                        self.finished = True
                    self.frontier.append(n)
                    self.grid.nodes[n].color_frontier = True

    def bfs_step(self):
        if not self.frontier:  # checks if frontier is empty
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.popleft()
        
        if current in self.explored: # if it is already explored
            return
        self.explored.add(current) # since we already checked if it's in explored, just push it
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        
        if current == self.grid.goal:  # if we've found the goal
            self.finished = True
            return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS] # this is a list of tuple for each move
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if (not self.grid.nodes[n].puddle) and (n not in self.explored) and (n not in self.frontier):
                    self.previous[n] = current
                    if n == self.grid.goal:
                        self.explored.add(n)
                        self.finished = True
                    self.frontier.append(n)
                    self.grid.nodes[n].color_frontier = True

    def ucs_step(self):
        if not self.frontier: # checks if frontier is empty
            self.failed = True
            self.finished = True
            print("no path")
            return
        current_cost, current = heappop(self.frontier_heap) # this will pop the lowest cost
        self.frontier.discard(current) # remove it in the tracker as well / i am using discard to avoid any unnecessary dup errors
        
        if current in self.explored: # if it is already explored
            return
        self.explored.add(current) # since we already checked if it's in explored, just push it
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        
        if current == self.grid.goal: # if we've found the goal
            self.finished = True
            return
        
        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if (not self.grid.nodes[n].puddle) and (n not in self.explored):
                    new_cost = current_cost + self.grid.nodes[n].cost() # grass: +10, else: +1
                    if new_cost < self.cost_dict.get(n, float('inf')): # .get will default return inf, if it doesn't exist / and cost_dict
                        self.cost_dict[n] = new_cost
                        self.previous[n] = current
                        heappush(self.frontier_heap, (new_cost, n))
                        self.frontier.add(n)
                        self.grid.nodes[n].color_frontier = True
    
    def astar_step(self):
        if not self.frontier: # checks if frontier is empty
            self.failed = True
            self.finished = True
            print("no path")
            return
        # heap stores (total_cost = actual_cost + heuristic , node)
        current_cost, current = heappop(self.frontier_heap) # pop the lowest total cost(real cost+hesuristic)
        self.frontier.discard(current) # remove it in the tracker as well / i am using discard to avoid any unnecessary dup errors
        
        if current in self.explored: # if it is already explored
            return
        self.explored.add(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        
        if current == self.grid.goal: # if we've found the goal
            self.finished = True
            return
        
        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if (not self.grid.nodes[n].puddle) and (n not in self.explored):
                    new_cost = self.cost_dict[current] + self.grid.nodes[n].cost() # grass: +10, else: +1
                    heuristic = abs(n[0] - self.grid.goal[0]) + abs(n[1] - self.grid.goal[1]) # heuristic value
                    new_total = new_cost + heuristic # total cost
                    if new_cost < self.cost_dict.get(n, float('inf')): # .get will default return inf, if it doesn't exist / and cost_dict
                        self.cost_dict[n] = new_cost
                        self.previous[n] = current
                        heappush(self.frontier_heap, (new_total, n))
                        self.frontier.add(n)
                        self.grid.nodes[n].color_frontier = True
