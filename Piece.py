#class representing game pieces, stores row, col, and player
class Piece:
  def __init__(self, player, row, col):
    self.player = player
    self.row = row
    self.col = col
  