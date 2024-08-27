import pdb
from random import randint
import time
from classes.end_the_game import EndTheGame
from classes.front import mousePositionCalculator
from classes.front_menu import promoteFront
from classes.pawn import Pawn
from classes.piece import Piece


class Player:
	def __init__(self, system_controlled, color, name="IA"):
		self.system_controlled = system_controlled
		self.name = name
		self.color = color
		self.historic_played_pieces = []

	# Função que reune as rotinas de uma jogada, separadas por rotina da IA ou do jogador humano.

	# Se for um jogador humano:
		# Sistema pede uma posição do jogador até encontrar a peça do movimento.
		# Sistema exibe as possibilidades de movimento da peça
		# Sistema pede uma coordenada para movimentar
		# Sistema tenta executar o movimento.

	# Se for uma IA:
		# Executa a função calcBetterMovement que retorna um par (peça, posição) para movimentar.
		# Sistema tenta executar o movimento.
		# Sistema entra em delay de alguns ms.

	def makeMove(self, table, front, janela, can_revert):
		piece = None
		object_clicked = None

		if not self.system_controlled:
			while object_clicked == None:
				mouse_entry = front.mouseReader(janela)
				object_clicked = front.findClickedComponent(mouse_entry, table, self.color, can_revert)
				if object_clicked != None:
					if isinstance(object_clicked, Piece):
						piece = object_clicked
						table.printTable(pieceSelected=piece)

						front.setCirclesOn(piece, table)
						front.drawCircles(table.positions)
						janela.update()

						mouse_entry = front.mouseReader(janela)
						position_entry = mousePositionCalculator(mouse_entry)

						piece.move(position_entry, table)
					else:
						if object_clicked == 1:
							table.revert()
							raise Exception
						elif object_clicked == 2:
							raise EndTheGame(-1)
		else:
			better_movement = self.calcBetterMovement(table)
			piece = better_movement[0]
			position_entry = better_movement[1]
			piece.move(position_entry, table)


		if isinstance(piece, Pawn) and piece.historic_positions[-1][2] == 'promotion':
			resp = 0

			if not self.system_controlled:
				resp = promoteFront(janela, front)
				front.rebuildScreen(janela)

			piece.promote(table, resp)

		if self.system_controlled:
			time.sleep(1)

	# Função que retorna o rei da cor do jogador (utilizado para facilitar as rotinas xeque e xeque-mate)
	def king(self, table):
		for piece in table.playerPieces(self.color):
			if (piece.name == self.color+'King'):
				return piece

		return None

	def undoMove(self, table):
		self.historic_played_pieces[-1].undo(table)

	# Função que retorna todas as possiveis movimentações de um jogador seguindo um par de (peça, lista de possiveis movimentações dessa peça)
	def possibleMovements(self, table):
		return_possibilities = []
		for piece in table.playerPieces(self.color):
			piece_available_positions = table.filterAvailablePositions(piece)
			if len(piece_available_positions) > 0:
				return_possibilities.append((piece, piece_available_positions))

		return return_possibilities

	# Função que verifica se o rei do jogador está sob ataque de alguma peça inimiga
	def underCheck(self, table):
		enemyColor = 1 if self.color == 'white' else 0
		enemy = table.players[enemyColor]
		king = self.king(table)

		for piece in table.playerPieces(enemy.color):
			if len(list(filter(lambda x: x[1] == king, piece.availablePositions(table)))) > 0:
				return True
		return False

	# Função que retorna o melhor movimento para a IA (deve ser incrementado com a inteligencia deterministica de movimentação)
	def calcBetterMovement(self, table):
		moves = self.possibleMovements(table)
		atack_movements = []
		for possibilities in moves:
			for move in possibilities[1]:
				if move[1] != None:
					atack_movements.append((possibilities[0], move[0], move[1]))

		if len(atack_movements) > 0:
			atack_movements.sort(key=lambda move: move[2].points, reverse=True)
			return (atack_movements[0][0], atack_movements[0][1])
		else:
			moves.sort(key=lambda move: move[0].points)
			movement = moves[randint(0, len(moves)-1)]
			piece = movement[0]
			position_entry = movement[1][randint(0, len(movement[1])-1)][0]
			return (piece, position_entry)