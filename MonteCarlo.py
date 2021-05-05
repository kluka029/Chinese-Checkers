#too slow, this implement depth-limited monte carlo
import random as rand
import Board as brd 
import Piece as pce 
import AlphaBeta as ab
import math
import time
from copy import deepcopy
import csv


class MonteCarlo:
  def __init__(self, board, player, depth, simulations):
    self.root = board
    self.player = player
    self.depth = depth
    self.simulations = simulations
    self.nodes_expanded = 0
    #self.n = n #number of times to play through
    #self.moves = m #number of moves per iteration

  
  #depth limited heuristic returns winning player
  def heuristic(self, state):
    if state.h1() < 0:
      return 2
    elif state.h1() > 0:
      return 1
    else:
      return 0


  #runs until win state is reached
  #assumes that player 1 uses h1 heuristic and player 2 uses h2 heuristic
  def simulate(self, state, player):
    def simulating(self, root, state, player, n):
      self.nodes_expanded += 1
      #generate children, pick state using heuristic
      if state.is_win() or n == 0:
        if state.pieces_in_goal(self.player) == 6:
          root.w += 1
        root.n += 1
        return 

      if state.children == []:
        state.generate_all_children(player)
      
      if player == 1:
        v = -99999
        best_state = state.children[0]
        for child in state.children:
          if child.h1() > v:
            v = child.v
            best_state = child
      else:
        v = 99999
        best_state = state.children[0]
        for child in state.children:
          if child.h1() < v:
            v = child.v
            best_state = child
      root.n += 1
      
      #best_state = rand.choice(state.children)
      
      #introduce small probability to pick suboptimal move
      '''
      if rand.random() < 0.05:
        best_state = rand.choice(state.children)
      '''
      

      #recursive call generates new move
      simulating(self, root, best_state, player%2 + 1, n-1)

    simulating(self, state, state, player, self.depth)


  #it's assumed that player 1 is h1, player 2 is h2
  def simulate_early_playout_term(self, state, player):
    def simulating(self, root, state, player, n):
      #generate children, pick state using heuristic
      if n == 0:
        if self.heuristic(state) == self.player:
          root.w += 1
        return 

      if state.children == []:
        state.generate_all_children(player)
      
      if player == 1:
        v = -9999
        best_state = state.children[0]
        for child in state.children:
          if child.h1() > v:
            v = child.v
            best_state = child
      else:
        v = 9999
        best_state = state.children[0]
        for child in state.children:
          if child.h2(player) < v:
            v = child.v
            best_state = child
      
      #best_state = rand.choice(state.children)

      '''
      #introduce small probability to pick suboptimal move
      if rand.random() < 0.05:
        best_state = rand.choice(state.children)
      '''

      #recursive call generates new move
      simulating(self, root, best_state, player%2 + 1, n-1)

    simulating(self, state, state, player, self.depth)


  def run(self):
    start = time.time() #start time
    end = 0

    #run for some time
    self.root.generate_all_children(self.player)
    n = 0
    while n < self.simulations:
      for child in self.root.children:
        self.nodes_expanded = 0
        start = time.time()
        self.simulate(child, self.player%2 + 1)
        end = time.time()
        '''
        with open('tmp.csv', 'a', newline='\n') as file:
          writer = csv.writer(file)
          writer.writerow([self.nodes_expanded, end-start])
        '''
      n += 1

    #choose node with best win percentage
    score = -99999
    best_move = self.root.children[0]
    for child in self.root.children:
      print(child.w/child.n)
      if child.w/child.n  > score:
        best_move = child
        score = child.w/child.n

    return best_move

'''
  #play one game 
  def play(self, state, player , x):
    print(f"x = {x}")
    print(f"score = {self.score}")
    if x > 0:
      if self.board.is_win():
        print("poopy")
      else:
        state.generate_all_children(player)
        n = rand.randrange(0, len(state.children), 1)
        newstate = state.children[n]
        self.board = deepcopy(newstate)
        self.board.print_board()
        print("\n")
        player = player % 2 + 1
        self.play(newstate, player, x-1)
    else:
      #manually change which function is called to get different heuristics
      self.score += state.h1(player) / self.repeats
      #self.score += self.h1(state, player)/self.repeats


  def play(self):
    def playing(self, state, player):
      #generate children, randomly pick new state
      state.generate_all_children(player)
      rand_idx = rand.randrange(0, len(state.children), 1)
      new_state = state.children[rand_idx]

      #get state that does not move pieces out of goal
      while new_state.pieces_in_goal(player) < state.pieces_in_goal(player):
        rand_idx = rand.randrange(0, len(state.children), 1)
        new_state = state.children[rand_idx]

      #return 1 if there is a win and player is 2
      if new_state.is_win() and player == 2:
        self.score += 1
      else:
        playing(self,new_state, player%2 + 1)

    playing(self, self.board, 2)
'''
      
'''
  #returns upper confidence bound for state
  def UCB1(self, state):
    if state.w == 0 and state.n == 0:
      return rand.random()
    return state.w / state.n + math.sqrt(2*math.log(state.parent.n)/state.n)


  #search until node is reached with no children
  def select_and_expand(self, state, player):
    state.generate_all_children(player)
    if state.children == []:
      return [state,player]
    else:
      ub = 0
      best_state = state
      for child in state.children:
        print(self.UCB1(child))
        if self.UCB1(child) > ub:
          best_state = child

      self.select_and_expand(best_state, player%2 + 1)


  def simulate_and_backpropagate(self, state, player):
    def simulating_and_backpropagating(self, state, player):
      #generate children, pick state using heuristic
      state.generate_all_children(player)
      if player == 1:
        v = 0
        best_state = state.children[0]
        for child in state.children:
          if child.h3(player) > v:
            best_state = child
      else:
        v = 0
        best_state = state.children[0]
        for child in state.children:
          if child.h3(player) < v:
            best_state = child

      #introduce small probability to pick suboptimal move
      if rand.random() < 0.05:
        best_state = rand.choice(state.children)

      #if there is a win, backpropagate, else get another move
      if best_state.is_win():
        parent = best_state.parent
        n = 1
        while parent != None:
          if n%2 == 0:
            parent.w += 1
          parent.n += 1
          n += 1
          parent = parent.parent

      else:
        simulating_and_backpropagating(self, best_state, player%2 + 1)

    simulating_and_backpropagating(self, state, player)


  #call play n times, update board score, return best move
  def run_UCB1(self):
    self.simulate_and_backpropagate(self.root, self.player)
    start = time.time() #start time

    #run for some time
    n = 0
    while time.time() - start < 1:
      n += 1
      [new_state, new_player] = self.select_and_expand(self.root, self.player)
      print("done")
      self.simulate_and_backpropagate(new_state, new_player)

    #choose node with highest number of playouts(n)
    n = 0
    best_move = self.root.children[0]
    for child in self.root.children:
      if child.n > n:
        best_move = child

    print(n)
    return best_move
'''
  
