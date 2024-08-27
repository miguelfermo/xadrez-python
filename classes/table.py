import pdb
from classes.bishop import Bishop
from classes.king import King
from classes.knight import Knight
from classes.pawn import Pawn
from classes.position import Position
from classes.queen import Queen
from classes.rook import Rook
from utils.prettyOutput import *

default_configuration = [
	['black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight', 'black_rook'],
	['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn'],
	[],
	[],
	[],
	[],
	['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn'],
	['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight', 'white_rook']
]


class Table:
  def __init__(self, self_position, initial_configuration=default_configuration):
    self.setInitialPositions()
    self.setInitialPieces(initial_configuration)
    self.self_position = self_position

  # Função que printa o tabuleiro atual.
  # Caso receba uma peça selecionada, vai mostrar visualmente as possibilidades de movimento e ataque daquela peça.
  def printTable(self, pieceSelected=None):
    print('-------------------------------------------------------------------------------------------------------------------')
    with prettyOutput(FG_CYAN) as out:
      out.write('  | {:11s} | {:11s} | {:11s} | {:11s} | {:11s} | {:11s} | {:11s} | {:11s} |'.format('0', '1', '2', '3',
                                                                                                    '4', '5', '6', '7'))
    for line in self.positions:
      print(self.positions.index(line), end='')
      for position in line:
        print(" | ", end='')

        empty_position = True
        for piece in self.pieces:
          if piece.actualPosition() == position.position:
            empty_position = False

            if pieceSelected != None and piece in list(map(lambda p: p[1], self.filterAvailablePositions(pieceSelected))):
              with prettyOutput(FG_RED) as out:
                out.write('{:11s}'.format(piece.name), end='')
              break

            if piece == pieceSelected:
              with prettyOutput(FG_GREEN) as out:
                out.write('{:11s}'.format(piece.name), end='')
              break

            piece_color = FG_BLUE if piece.color == 'black' else FG_CYAN
            with prettyOutput(piece_color) as out:
              out.write('{:11s}'.format(piece.name), end='')
            break

        if empty_position:
          def returnEmptyMovePositions(position):
            if (position[2] != "en_passant"):
              return position[0]

          def returnEnPassantPositions(position):
            if (position[2] == "en_passant"):
              return position[0]

          if pieceSelected != None and position.position in list(map(returnEmptyMovePositions, self.filterAvailablePositions(pieceSelected))):
            with prettyOutput(FG_GREEN) as out:
              out.write('     *     ', end='')

          elif pieceSelected != None and position.position in list(map(returnEnPassantPositions, self.filterAvailablePositions(pieceSelected))):
            with prettyOutput(FG_YELLOW) as out:
              out.write('     *     ', end='')

          else:
            with prettyOutput(FG_WHITE) as out:
              out.write('     -     ', end='')

      print (" |")
    print('-------------------------------------------------------------------------------------------------------------------')

  # Função que inicializa as posições de um tabuleiro em uma matriz de posições brancas e pretas.
  def setInitialPositions(self):
    positions = []
    for i in range(0, 8, 1):
      line = []
      for j in range(0, 8, 1):
        color = 'black' if (i%2 == 0 and j%2 != 0) or (i%2 != 0 and j%2 == 0) else 'white'
        line.append(Position(color, (j, i)))
      positions.append(line)

    self.positions = positions

  # Função que inicializa as peças de um tabuleiro uma distribuição informada em initial_configuration.
  def setInitialPieces(self, initial_configuration):
    pieces = []
    for i in range(0, 8, 1):
      list = initial_configuration[i]
      for j in range(0, len(list), 1):
        item = list[j]
        if(item != None):
          splitted_str = item.split('_')
          color = splitted_str[0]
          piece_subclass = splitted_str[1]
          initial_position = (j, i)

          if piece_subclass == 'rook':
            pieces.append(Rook(color, [(initial_position, None, None)]))
          elif piece_subclass == 'knight':
            pieces.append(Knight(color, [(initial_position, None, None)]))
          elif piece_subclass == 'bishop':
            pieces.append(Bishop(color, [(initial_position, None, None)]))
          elif piece_subclass == 'queen':
            pieces.append(Queen(color, [(initial_position, None, None)]))
          elif piece_subclass == 'king':
            pieces.append(King(color, [(initial_position, None, None)]))
          elif piece_subclass == 'pawn':
            pieces.append(Pawn(color, [(initial_position, None, None)]))
    self.pieces = pieces

  # Retorna uma peça baseado em um par (x, y) de uma posição.
  # É possivel limitar a cor do conjunto de peças a ser procurada, passando o parametro color como 'white' ou 'black'.
  def findPiece(self, position, color='both'):
    if (color == 'both'):
      for piece in self.pieces:
        if piece.actualPosition() == position:
          return piece
    else:
      for piece in self.playerPieces(color):
        if piece.actualPosition() == position:
          return piece

  # Retorna as peças atuais no tabuleiro de uma cor
  def playerPieces(self, playerColor):
    return list(filter(lambda piece: piece.color == playerColor, self.pieces))

  # Função que limita as possibilidades de movimento de uma peça pela configuração atual do tabuleiro sob os seguintes parametros:
    # Movimentos que coloquem seu Rei sob xeque são descartados.
    # Caso o Rei esteja sob xeque, movimentos que não o tirem de xeque são descartados.
  def filterAvailablePositions(self, piece):
    playerColor = 0 if piece.color == 'white' else 1
    player = self.players[playerColor]
    filtered_possibilities = []

    for possibility in piece.availablePositions(self):
      piece.move(possibility[0], self, ignore_check=True)
      if not player.underCheck(self):
        filtered_possibilities.append(possibility)
      piece.undo(self)
    return filtered_possibilities

  def replacePiece(self, piece_subclass, old_piece):
    if piece_subclass == 0:
      piece = Queen(old_piece)
    elif piece_subclass == 1:
      piece = Rook(old_piece)
    elif piece_subclass == 2:
      piece = Knight(old_piece)
    elif piece_subclass == 3:
      piece = Bishop(old_piece)
    else:
      piece = Pawn(old_piece)

    self.pieces.append(piece)
    self.pieces.remove(old_piece)
    return piece

  def playerOfColor(self, color):
    playerIndex = 1 if color == 'black' else 0
    return self.players[playerIndex]

  def revert(self):
    self.players[0].undoMove(self)
    self.players[1].undoMove(self)