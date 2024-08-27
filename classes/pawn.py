import pdb
import random
from classes.bishop import Bishop
from classes.knight import Knight
from classes.piece import Piece
from classes.queen import Queen
from classes.rook import Rook

class Pawn (Piece):
  def __init__(self, *args):
    self.points = 1
    self.promoted_to = None
    if len(args) == 2:
      self.image_file = './assets/' + args[0] + 'Pawn.png'
      super().__init__(self.image_file, args[0], args[1])
    elif len(args) == 1:
      self.image_file = './assets/' + args[0].color + 'Pawn.png'
      super().__init__(self.image_file, args[0].color, args[0].historic_positions)


  def move(self, position_entry, table, ignore_check=False):
    if Piece.validPosition(position_entry):
      positions = table.filterAvailablePositions(self) if not ignore_check else self.availablePositions(table)

      for position in positions: # Position é [(x, y), peca_atacada, movimento_especial]
        if position[0] == position_entry:
          if (position[1] != None):
            table.pieces.remove(position[1])
          self.historic_positions.append(position)

          table.playerOfColor(self.color).historic_played_pieces.append(self)
          return self
    raise Exception

  def promote(self, table, class_identifier):
    if class_identifier == 0:
      new_piece = Queen(self)
    elif class_identifier == 1:
      new_piece = Rook(self)
    elif class_identifier == 2:
      new_piece = Bishop(self)
    elif class_identifier == 3:
      new_piece = Knight(self)

    self.__init__(new_piece)
    self.promoted_to = new_piece
    self.name = new_piece.name
    super().__init__(new_piece.image_file, self.color, self.historic_positions)

  def undo(self, table):
    if len(table.playerOfColor(self.color).historic_played_pieces) > 0:
      trash = self.historic_positions[-1]
      if trash[1] != None:
        table.pieces.append(trash[1])

      if trash[2] == "promotion":
        new_piece = Pawn(self)
        self.__init__(new_piece)
        self.promoted_to = None
        self.name = new_piece.name
        super().__init__(new_piece.image_file, self.color, self.historic_positions)

      self.historic_positions.pop()

      if table.playerOfColor(self.color).historic_played_pieces[-1] == self:
        table.playerOfColor(self.color).historic_played_pieces.pop()

  # Retorna um array de posição onde o primeiro indice é uma posição valida para se movimentar e o segundo indice uma peça inimiga que pode ser atacada.
  def availablePositions(self, table):
    return_possibilities = []
    if self.promoted_to != None:
      return_possibilities = self.promoted_to.availablePositions(table)
    else:
      if (self.color == 'black'):
        for i in (-1, 1):
          new_position = (self.actualPosition()[0] + i, self.actualPosition()[1] + 1)
          other_piece = table.findPiece(new_position)
          if other_piece != None and other_piece.color != self.color:
            if new_position[1] == 7:
              return_possibilities.append([new_position, other_piece, "promotion"])
            else:
              return_possibilities.append([new_position, other_piece, None])

        for i in (-1, 1):
          new_position = (self.actualPosition()[0] + i, self.actualPosition()[1] + 1)
          attack_position = (self.actualPosition()[0] + i, self.actualPosition()[1])
          other_piece = table.findPiece(attack_position)
          if other_piece != None and other_piece.name == 'whitePawn' and len(table.players[0].historic_played_pieces) > 0:
            last_played_piece = table.players[0].historic_played_pieces[-1]
            if last_played_piece == other_piece:
              return_possibilities.append([new_position, other_piece, "en_passant"])

        if (len(self.historic_positions) > 1):
          new_position = (self.actualPosition()[0], self.actualPosition()[1] + 1)
          other_piece = table.findPiece(new_position)
          if Piece.validPosition(new_position):
            if other_piece == None:
              if new_position[1] == 7:
                return_possibilities.append([new_position, other_piece, "promotion"])
              else:
                return_possibilities.append([new_position, other_piece, None])
        else:
          new_position = (self.actualPosition()[0], self.actualPosition()[1] + 1)
          other_piece = table.findPiece(new_position)
          if Piece.validPosition(new_position) and other_piece == None:
            if new_position[1] == 7:
              return_possibilities.append([new_position, other_piece, "promotion"])
            else:
              return_possibilities.append([new_position, other_piece, None])
            new_position = (self.actualPosition()[0], self.actualPosition()[1] + 2)
            other_piece = table.findPiece(new_position)
            if Piece.validPosition(new_position) and other_piece == None:
              if new_position[1] == 7:
                return_possibilities.append([new_position, other_piece, "promotion"])
              else:
                return_possibilities.append([new_position, other_piece, None])


      else:
        for i in (-1, 1):
          new_position = (self.actualPosition()[0] + i, self.actualPosition()[1] - 1)
          other_piece = table.findPiece(new_position)
          if other_piece != None and other_piece.color != self.color:
            if new_position[1] == 0:
              return_possibilities.append([new_position, other_piece, "promotion"])
            else:
              return_possibilities.append([new_position, other_piece, None])

        for i in (-1, 1):
          new_position = (self.actualPosition()[0] + i, self.actualPosition()[1] - 1)
          attack_position = (self.actualPosition()[0] + i, self.actualPosition()[1])
          other_piece = table.findPiece(attack_position)
          if other_piece!= None and other_piece.name == 'blackPawn' and len(table.players[1].historic_played_pieces) > 0:
            last_played_piece = table.players[1].historic_played_pieces[-1]
            if last_played_piece == other_piece:
              return_possibilities.append([new_position, other_piece, "en_passant"])

        if (len(self.historic_positions) > 1):
          new_position = (self.actualPosition()[0], self.actualPosition()[1] - 1)
          other_piece = table.findPiece(new_position)
          if Piece.validPosition(new_position) and other_piece == None:
            if new_position[1] == 0:
              return_possibilities.append([new_position, other_piece, "promotion"])
            else:
              return_possibilities.append([new_position, other_piece, None])
        else:
          new_position = (self.actualPosition()[0], self.actualPosition()[1] - 1)
          other_piece = table.findPiece(new_position)
          if Piece.validPosition(new_position) and other_piece == None:
            if new_position[1] == 0:
              return_possibilities.append([new_position, other_piece, "promotion"])
            else:
              return_possibilities.append([new_position, other_piece, None])
            new_position = (self.actualPosition()[0], self.actualPosition()[1] - 2)
            other_piece = table.findPiece(new_position)
            if Piece.validPosition(new_position) and other_piece == None:
              if new_position[1] == 0:
                return_possibilities.append([new_position, other_piece, "promotion"])
              else:
                return_possibilities.append([new_position, other_piece, None])

    return return_possibilities