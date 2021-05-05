import Piece as pc
from copy import deepcopy
import math
import MonteCarlo as mc
import gc

class Board:
  def __init__(self, parent=None):
    self.reached = False
    self.w = 0 #wins, used for monte carlo
    self.n = 0 #visits, used for monte carlo
    self.v = 0 #heuristic value, used for minimax
    self.alpha = -9999999 #local alpha for minimax
    self.beta = 9999999 #local beta for minimax

    #used to print game state
    self.board = [[0, 0, 0, 0, 2, 2, 2],
                  [0, 0, 0, 0, 0, 2, 2],
                  [0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0],
                  [1, 1, 0, 0, 0, 0, 0],
                  [1, 1, 1, 0, 0, 0, 0]]

    #player 1's pieces
    self.p1_pieces = [pc.Piece(1,4,0),
                      pc.Piece(1,5,0),
                      pc.Piece(1,5,1),
                      pc.Piece(1,6,0),
                      pc.Piece(1,6,1),
                      pc.Piece(1,6,2)]

    #player 2's pieces
    self.p2_pieces = [pc.Piece(2,0,4),
                      pc.Piece(2,0,5),
                      pc.Piece(2,0,6),
                      pc.Piece(2,1,5),
                      pc.Piece(2,1,6),
                      pc.Piece(2,2,6)]

    #list of Board's representing all valid moves for current player
    self.children = []

    #parent Board
    self.parent = parent
  
  
  #prints game state
  def print_board(self):
    for i in range(0,7):
      print(self.board[i])
    

  #get element of board at row, col
  def get_element(self, row, col):
    return self.board[row][col]


  #prints game state for interface
  def print_board_interface(self, row, col):
    temp = self.board[row][col]
    self.board[row][col] = 3
    for i in range(0,7):
      print(self.board[i])
    self.board[row][col] = temp


  #updates board 
  def update_board(self, player, piece_idx,  new_row, new_col):
    if player == 1:
      piece = self.p1_pieces[piece_idx]
    else:
      piece = self.p2_pieces[piece_idx]
    self.board[piece.row][piece.col] = 0
    self.board[new_row][new_col] = piece.player
    piece.row = new_row
    piece.col = new_col


  #check if win
  def is_win(self):
    return ((self.board[4][0] == 2 and 
            self.board[5][0] == 2 and 
            self.board[5][1] == 2 and 
            self.board[6][0] == 2 and 
            self.board[6][1] == 2 and 
            self.board[6][2] == 2) or 
            (self.board[0][4] == 1 and 
            self.board[0][5] == 1 and 
            self.board[0][6] == 1 and 
            self.board[1][5] == 1 and 
            self.board[1][6] == 1 and 
            self.board[2][6] == 1))


  #returns number of pieces that player has in goal
  def pieces_in_goal(self, player):
    num = 0
    if player == 1:
      rows = [0,0,0,1,1,2]
      cols = [4,5,6,5,6,6]
      for i in range(6):
        if self.board[rows[i]][cols[i]] == 1:
          num += 1
    else:
      rows = [4,5,5,6,6,6]
      cols = [0,0,1,0,1,2]
      for i in range(6):
        if self.board[rows[i]][cols[i]] == 2:
          num += 1

    return num
    

  #searches for all possible moves from current Board for appropriate player, adds these Boards to children
  def generate_children(self, piece, idx, player, row, col, arr):
    row_nums = [-1, 0, 1, 1, 0, -1]
    col_nums = [0, 1, 1, 0, -1, -1]

    for i in range(0,6):
      new_row = row + row_nums[i]
      new_col = col + col_nums[i]
      
      #jumping case
      if self.get_element(row, col) == 0:
        if new_row <= 6 and new_col <= 6 and new_row >= 0 and new_col >= 0 and self.get_element(new_row,new_col) != 0:
          new_row += row_nums[i]
          new_col += col_nums[i]
          if not (new_row > 6 or new_col > 6 or new_row < 0 or new_col < 0 or self.get_element(new_row,new_col) != 0):
            newBoard = Board(self.board)
            newBoard.board = deepcopy(self.board)
            newBoard.p1_pieces = deepcopy(self.p1_pieces)
            newBoard.p2_pieces = deepcopy(self.p2_pieces)
            newBoard.update_board(player, idx, new_row, new_col)
            add = True
            for child in self.children:
              if child.board == newBoard.board:
                add = False

            if add:
              arr.append(newBoard)
              newBoard.parent = self
              self.children.append(newBoard)
              self.generate_children(piece, idx, player, new_row, new_col, arr)

      #normal case(no jumps)
      else:
        #if there is an open space, append this move to children(regular case)
        if not (new_row > 6 or new_col > 6 or new_row < 0 or new_col < 0 or self.get_element(new_row,new_col) != 0):
          newBoard = Board(self.board)
          newBoard.board = deepcopy(self.board)
          newBoard.p1_pieces = deepcopy(self.p1_pieces)
          newBoard.p2_pieces = deepcopy(self.p2_pieces)
          newBoard.update_board(player, idx, new_row, new_col)
          arr.append(newBoard)
          newBoard.parent = self
          self.children.append(newBoard)

        #if space beyond space is open, search from this open position(jumping case)
        else:
          new_row += row_nums[i]
          new_col += col_nums[i]
          if not (new_row > 6 or new_col > 6 or new_row < 0 or new_col < 0 or self.get_element(new_row,new_col) != 0):
            newBoard = Board(self.board)
            newBoard.board = deepcopy(self.board)
            newBoard.p1_pieces = deepcopy(self.p1_pieces)
            newBoard.p2_pieces = deepcopy(self.p2_pieces)
            newBoard.update_board(player, idx, new_row, new_col)
            arr.append(newBoard)
            newBoard.parent = self
            self.children.append(newBoard)
            self.generate_children(piece, idx, player, new_row, new_col, arr)


  #generate all children 
  def generate_all_children(self, player):
    self.children = []
    if player == 1:
      pieces = self.p1_pieces
    else:
      pieces = self.p2_pieces
    for i in range(6):
      self.generate_children(pieces[i], i, player, pieces[i].row, pieces[i].col, [])

      
  #heuristics
  #returns squared sum of distances of pieces from end point
  def A(self, player):
    self.reached = True
    f = 0
    if player == 1:
      for piece in self.p1_pieces:
        f += ((piece.row**2 + (6-piece.col)**2)**(1/2))**2
    else:
      for piece in self.p2_pieces:
        f += (((6-piece.row)**2 + piece.col**2)**(1/2))**2

    return f


  #returns squared sum of distance of pieces to diagonal(bottom left to top right)
  def B(self, player):
    if player == 1:
      pieces = self.p1_pieces
    else:
      pieces = self.p2_pieces

    v = 0
    for piece in pieces:
      v += (abs(piece.row - piece.col) / math.sqrt(2))**2

    return v


  #maximum 'vertical' displacement(furthest diagonal)
  def C(self, player):
    v = 0
    if player == 1:
      for piece in self.p1_pieces:
        if piece.row - piece.col + 6 > v:
          v = piece.row - piece.col + 6
    else:
      for piece in self.p2_pieces:
        if piece.col - piece.row + 6 > v:
          v = piece.col - piece.row + 6

    return v


  #good
  #weighted sum heuristic found in source 3 of the paper
  def h1(self):
    w1 = 0.911
    w2 = 0.140
    w3 = 0.388
    self.v = w1*(self.A(2)-self.A(1)) + w2*(self.B(2)-self.B(1)) + w3*(self.C(1)-self.C(2))
    return self.v


  #good
  #displacement from past state heuristic found in source 4 of the paper
  def h2(self, player):
    self.reached = True
    f = 0
    if player == 1:
      for i, piece in enumerate(self.p1_pieces):
        f += (self.parent.p1_pieces[i].row - piece.row) + (piece.col - self.parent.p1_pieces[i].col)
    else:
      for i, piece in enumerate(self.p2_pieces):
        f += (self.parent.p2_pieces[i].row - piece.row) + (piece.col - self.parent.p2_pieces[i].col)
    self.v = f
    return f


  '''
  #locality (how many other pieces are right next to you, more jumping possible)
  def h2(self, player):
    self.reached = True
    def count_pieces(self, piece):
      f = 0
      row_nums = [-1, 0, 1, 1, 0, -1]
      col_nums = [0, 1, 1, 0, -1, -1]
      for row in row_nums:
        for col in col_nums:
          if self.board[piece.row + row, piece.col + col] != 0:
            f += 1
      return f

    h = 0 
    if player == 1:
      for piece in self.p1_pieces: 
        h += count_pieces(piece)
    if player == 2: 
      for piece in self.p2_pieces:
        h += count_pieces(piece)
    h = h/6 #normalize by number of pieces
    self.v = h
    return h
    '''
