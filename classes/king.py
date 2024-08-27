import pdb
from classes.piece import Piece

class King(Piece):
  def __init__(self, *args):
    self.points = 150
    if len(args) == 2:
      self.image_file = './assets/' + args[0] + 'King.png'
      super().__init__(self.image_file, args[0], args[1])
    elif len(args) == 1:
      self.image_file = './assets/' + args[0].color + 'King.png'
      super().__init__(self.image_file, args[0].color, args[0].historic_positions)

  def undo(self, table):
    if self.historic_positions[-1][1] != None:
      table.pieces.append(self.historic_positions[-1][1])
    table.playerOfColor(self.color).historic_played_pieces.pop()

    if self.historic_positions[-1][2] != None:
      self.historic_positions[-1][3].historic_positions.pop()

    self.historic_positions.pop()

  def move(self, position_entry, table, ignore_check=False):
    if Piece.validPosition(position_entry):
      positions = table.filterAvailablePositions(self) if not ignore_check else self.availablePositions(table)

      for position in positions: #position é [(x, y), peca_atacada, movimento_especial, torre_a_se_movimentar]
        if position[0] == position_entry:
          if (position[2] != None):
            rook = position[3]
            position_rook = position[0][0] + (1 if position[2] == "long_castling" else -1)
            rook.historic_positions.append([(position_rook, position[0][1]), None, None])

          if (position[1] != None):
            table.pieces.remove(position[1])

          table.playerOfColor(self.color).historic_played_pieces.append(self)
          self.historic_positions.append(position)
          return self
    raise Exception



  # Retorna um array de posição onde o primeiro indice é uma posição valida para se movimentar e o segundo indice uma peça inimiga que pode ser atacada.
  # Usar sempre a função table#filterAvailablePositions para garantir que as possibilidades sejam filtradas pela configuração atual do tabuleiro.
  def availablePositions(self, table):
    return_possibilities = []
    for sum_y in (-1, 0, 1):
      for sum_x in (-1, 0, 1):
        if sum_x == 0 and sum_y == 0:
          continue
        new_position_x = self.actualPosition()[0] + sum_x
        new_position_y = self.actualPosition()[1] + sum_y
        new_position = (new_position_x, new_position_y)
        other_piece = table.findPiece(new_position)

        if Piece.validPosition(new_position) and other_piece == None:
          return_possibilities.append([new_position, other_piece, None])
        elif other_piece != None and other_piece.color != self.color:
          return_possibilities.append([new_position, other_piece, None])

    if (len(self.historic_positions) < 2):
      if self.color == 'white':
        long_rook = table.findPiece((0, 7), self.color)
        long_rook_castling_available = False
        if (long_rook is not None) and (len(long_rook.historic_positions) < 2):
          long_rook_castling_available = True
          for x in range(1, 4):
            if table.findPiece((x, 7), self.color) is not None:
              long_rook_castling_available = False
              break
        short_rook = table.findPiece((7, 7), self.color)
        short_rook_castling_available = False
        if (short_rook is not None) and (len(short_rook.historic_positions) < 2):
          short_rook_castling_available = True
          for x in range(5, 7):
            if table.findPiece((x, 7), self.color) is not None:
              short_rook_castling_available = False
              break

        if long_rook_castling_available:
          return_possibilities.append([(2, 7), None, "long_castling", long_rook])

        if short_rook_castling_available:
          return_possibilities.append([(6, 7), None, "short_castling", short_rook])

      else:
        long_rook = table.findPiece((0, 0), self.color)
        long_rook_castling_available = False
        if (long_rook is not None) and (len(long_rook.historic_positions) < 2):
          long_rook_castling_available = True
          for x in range(1, 4):
            if table.findPiece((x, 0), self.color) is not None:
              long_rook_castling_available = False
              break

        short_rook = table.findPiece((7, 0), self.color)
        short_rook_castling_available = False
        if (short_rook is not None) and (len(short_rook.historic_positions) < 2):
          short_rook_castling_available = True
          for x in range(5, 7):
            if table.findPiece((x, 0), self.color) is not None:
              short_rook_castling_available = False
              break

        if long_rook_castling_available:
          return_possibilities.append([(2, 0), None, "long_castling", long_rook])

        if short_rook_castling_available:
          return_possibilities.append([(6, 0), None, "short_castling", short_rook])


    return return_possibilities