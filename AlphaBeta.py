#h2 only works for depth = 1!!!

import random as rand
import time


class AlphaBeta:
  def __init__ (self, board, depth = 1): 
    self.search_depth = depth
    self.alpha = -9999999
    self.beta = 9999999
    self.root = board #root node
    self.best_move = board #set best move to board as default
    self.root_nodes = 0
    self.non_root_nodes = 0
    self.b = 0
    self.explored = 0


  #generates children for all nodes from root to search_depth
  def initialize_minimax(self, nodes, player = 1, level = 0):
    if level < self.search_depth:
      for node in nodes:  
        if node.children == []:
          node.generate_all_children(player)
        self.initialize_minimax(node.children, player % 2 + 1, level + 1)


  #returns the average branching factor
  def average_branching_factor(self):
    def factoring(self, node):
      if node.children != []:
        self.root_nodes += 1
        for child in node.children:
          factoring(self, child)
          
      self.non_root_nodes += 1
    factoring(self, self.root)

    self.b = (self.non_root_nodes - 1) / self.root_nodes
    return self.b


  #'free' memory
  def free(self, nodes, player = 1, level = 0):
    if level < self.search_depth:
      for node in nodes:
        if node.children != []:
          self.free(node.children, player % 2 + 1, level + 1)
        node.children = []

        
  #alpha beta
  def run_alphaBeta(self,player):
    #generate children
    self.root.children = []
    start = time.time()
    self.initialize_minimax([self.root], player, 0)
    end = time.time()
    print(f"node generation time = {end - start})")

    #performs alpha beta for a subtree, passes max(player 1) or min(player 2) up to root
    def running(self, root, player):
      if root.children == []:             #bottom level has no children, so call heuristic and return v
        root.h1()
      else:                               #otherwise we need to pass v up from the children
        if player == 1:                   #look for max(player 1)
          root.v = -99999
          for child in root.children:
            child.alpha = root.alpha
            child.beta = root.beta
            if running(self, child, player%2+1) >= root.beta:
              root.v = child.v
              break
            else:
              root.alpha = max(root.alpha, child.v)
              if child.v > root.v:
                root.v = child.v
        else:                             #look for min(player 2)
          root.v = 99999
          for child in root.children:
            child.alpha = root.alpha
            child.beta = root.beta
            if running(self, child, player%2+1) <= root.alpha:
              root.v = child.v
              break
            else:
              root.beta = min(root.beta, child.v)
              if child.v < root.v:
                root.v = child.v
      self.explored += 1
                             
      return root.v
    #call running and get best_move from children of root
    start = time.time()
    running(self, self.root, player)
    end = time.time()
    print(f"search time = {end - start}")
    if player == 1:
      v = -99999
      for child in self.root.children:
        if child.v > v:
          v = child.v
          self.best_move = child
    else:
      v = 99999
      for child in self.root.children:
        if child.v < v:
          v = child.v
          self.best_move = child
    #introduce some small probability to pick sub-optimal move to prevent draw states(two player minimax does not work without this)
    #if rand.random() < 0.05:
    #  self.best_move = rand.choice(self.root.children)


  #minimax with h1 heuristic
  def run_minimax_h1(self,player):
    #generate children
    self.root.children = []
    start = time.time()
    self.initialize_minimax([self.root], player, 0)
    end = time.time()
    print(f"node generation time = {end - start}")

    #performs minimax for a subtree, passes max(player 1) or min(player 2) up to root
    def running(self, root, player):
      if root.children == []:             #bottom level has no children, so call heuristic and return v
        root.h1()
      else:                               #otherwise we need to pass v up from the children
        if player == 1:                   #look for max(player 1)
          root.v = -99999 
          for child in root.children:
            if running(self, child, player%2 + 1) > root.v:
              root.v = child.v
        else:                             #look for min(player 2)
          root.v = 99999
          for child in root.children:
            if running(self, child, player%2 + 1) < root.v:
              root.v = child.v
      self.explored += 1

      return root.v
    #call running and get best_move from children of root
    start = time.time()
    running(self, self.root, player)
    end = time.time()
    print(f"search time = {end -start}")
    if player == 1:
      v = -99999
      for child in self.root.children:
        if child.v > v:
          v = child.v
          self.best_move = child
    else:
      v = 99999
      for child in self.root.children:
        print(child.v)
        if child.v < v:
          v = child.v
          self.best_move = child
    #introduce some small probability to pick sub-optimal move to prevent draw states(two player minimax does not work without this)
    #if rand.random() < 0.05:
    #  self.best_move = rand.choice(self.root.children)


  #minimax with h2 heuristic
  def run_minimax_h2(self,player):
    #generate children
    self.root.children = []
    self.initialize_minimax([self.root], player, 0)

    #performs minimax for a subtree, passes max(player 1) or min(player 2) up to root
    def running(self, root, player):
      if root.children == []:             #bottom level has no children, so call heuristic and return v
        root.h2(player%2 + 1)
      else:                               #otherwise we need to pass v up from the children
        if player == 1:                   #look for max(player 1)
          root.v = -99999 
          for child in root.children:
            if running(self, child, player%2 + 1) > root.v:
              root.v = child.v
        else:                             #look for min(player 2)
          root.v = 99999
          for child in root.children:
            if running(self, child, player%2 + 1) < root.v:
              root.v = child.v

      return root.v
    #call running and get best_move from children of root
    running(self, self.root, player)
    if player == 1:
      v = -99999
      rand.shuffle(self.root.children)
      for child in self.root.children:
        if child.v > v:
          v = child.v
          self.best_move = child
    else:
      v = 99999
      rand.shuffle(self.root.children)
      for child in self.root.children:
        if child.v < v:
          v = child.v
          self.best_move = child
