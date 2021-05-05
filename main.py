'''
To do:
-show that monte carlo is too slow to be implemented as the sole algorithm(only makes sense to do one sim with guided play)
  -get average number of nodes expanded/time of simulation for random and guided playout
-show that early playout termination is ineffective as any heuristic that is not the win state is fallible
-test monte carlo against h2(benchmark)
-do 20? tests of h1,depth3 against human players. record number of losing moves(using h2)
'''
import Board as brd
import MonteCarlo as monte
import AlphaBeta as ab
import Piece as pc
import random as rand 
import sys
import time
import csv
from copy import deepcopy
import gc
sys.setrecursionlimit(100000000)


#function to write stats to file
def export_stats(h, depth, moves, winner, mode, file):
  stats = open(file, "a")
  stats.write(f"{h}, {depth}, {moves}, {winner}, {mode} \n")


#returns random child from state
def random_agent(player, state, depth):
  if player == 1:
    pieces = state.p1_pieces
  else:
    pieces = state.p2_pieces
  while state.children == []:
    idx = rand.randint(0,5)
    piece = pieces[idx]
    state.generate_children(piece, idx, player, piece.row, piece.col, [])
  next_move = rand.choice(state.children)
  return next_move


#returns child chosen by human player
def human_agent(player, state, depth):
  n = 0
  piece = pc.Piece
  userInput = 'n'
  #have user pick piece to move
  while userInput != 'y':
    if player == 1:
      piece = state.p1_pieces[n]
    else:
      piece = state.p2_pieces[n]
    state.print_board_interface(piece.row,piece.col)
    n = (n + 1) % 6
    print("Accept piece?(y/n)")
    userInput = input()

  arr = []
  state.children = []
  state.generate_children(piece, n-1, player, piece.row, piece.col, arr)
  n = 0
  userInput = 'n'
  #have user pick location to move to
  print(f"number of children = {len(state.children)}")
  while userInput != 'y':
    arr[n].print_board()
    n = (n + 1) % len(arr)
    print("Accept move?(y/n)")
    userInput = input()

  #'dereference' memory
  state.children = []
  return arr[n-1]


#returns child using monte carlo
def monteCarlo_agent(player, state, depth):
  m = monte.MonteCarlo(state, player, depth, 1)
  #a = ab.AlphaBeta(deepcopy(state))
  #a.initialize_minimax([a.root], player, 2)
  start = time.time()
  tmp = m.run()
  end = time.time()
  print(f"monte carlo time = {end-start}")
  '''
  with open('monteCarlo.csv', 'a', newline='\n') as file:
    writer = csv.writer(file)
    writer.writerow([a.average_branching_factor(), end-start])
  '''
  return tmp


#returns child using minimax
def minimax_agent_h1(player, state, depth):
  a = ab.AlphaBeta(state, depth)
  start = time.time()
  a.run_minimax_h1(player)
  end = time.time()
  '''
  with open('minimax_speed.csv', 'a', newline='\n') as file:
    writer = csv.writer(file)
    writer.writerow([a.average_branching_factor(), end-start])
  '''
  print(f"explored = {a.explored}")
  return a.best_move


#returns child using minimax
def minimax_agent_h2(player, state, depth):
  a = ab.AlphaBeta(state, depth)
  start = time.time()
  a.run_minimax_h2(player)
  end = time.time()
  '''
  with open('minimax_speed.csv', 'a', newline='\n') as file:
    writer = csv.writer(file)
    writer.writerow([a.average_branching_factor(), end-start])
  '''
  return a.best_move


#returns child using alpha beta
def alphaBeta_agent(player, state, depth):
  a = ab.AlphaBeta(state, depth)
  start = time.time()
  a.run_alphaBeta(player)
  end = time.time()
  print(f"explored = {a.explored}")
  return a.best_move


#carry out gameplay. takes two agent functions as its argument
def play(player1_agent, player2_agent, max_moves, depth1 = 1, depth2 = 1):
  moves = 0
  gameBoard = brd.Board()               
  player = 1
  #mode = "random vs. mc, iterations = 5, depth = 10"
  #h = "h3"
  #depth = int(10)

  #game loop
  while not gameBoard.is_win() and moves < max_moves:
    #player 1's turn
    if player == 1:
      print("player 1's turn: \n")
      gameBoard = player1_agent(player, gameBoard, depth1)

    else:
      print("player 2's turn: \n")
      gameBoard = player2_agent(player, gameBoard, depth2)
    gameBoard.print_board()
    player = player % 2 + 1
    moves += 1
    print(moves)

  #determine if there is winner or not, calculate losing moves for loser
  losing_moves = 0
  del gameBoard.children
  gc.collect()
  if gameBoard.is_win():
    winner = player%2 + 1
    loser = player
    while gameBoard.pieces_in_goal(loser) != 6:
      gameBoard = minimax_agent_h2(loser, gameBoard, 1)
      losing_moves += 1
    print (f"winner: player {winner}")
    return winner, moves, losing_moves
  else:
    return 0, moves, losing_moves


'''
def test (p1agent, p2agent, n, h, depth, max_moves):
  match p1agent:
    case human_agent:
      mode = "Human-"
    case minimax_agent: 
      mode = "Minimax-"
    case random_agent:
      mode = "Random-"
    case monteCarlo_agent:
      mode = "Monte Carlo-"
    case alphaBeta_agent: 
      mode = "Alpha-Beta-"
  match p2agent:
    case human_agent:
      mode += "Human"
    case minimax_agent: 
      mode += "Minimax"
    case random_agent:
      mode += "Random"
    case monteCarlo_agent:
      mode += "Monte Carlo"
    case alphaBeta_agent: 
      mode += "Alpha-Beta"
  for i in range(n):
    end_state = play (p1agent, p2agent, max_moves, depth)
    export_stats (h, depth, end_state[1], end_state[0], mode, "stats.csv")
'''


#call play function
def main():
  #test speed of win for different heuristics and depths
  start = time.time()
  for i in range(1):
    [winner, moves, losing_moves] = play(monteCarlo_agent, human_agent, 200, 200, 1)
    with open('tmp.csv', 'a', newline='\n') as file:
      writer = csv.writer(file)
      writer.writerow([winner, moves, losing_moves])
  end = time.time()
  print(f"time elapsed = {end - start}")


if __name__ == '__main__':
  main()
