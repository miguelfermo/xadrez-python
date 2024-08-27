from classes.piece import Piece


class Queen(Piece):
	def __init__(self, *args):
		self.points = 50
		if len(args) == 2:
			self.image_file = './assets/' + args[0] + 'Queen.png'
			super().__init__(self.image_file, args[0], args[1])
		elif len(args) == 1:
			self.image_file = './assets/' + args[0].color + 'Queen.png'
			super().__init__(self.image_file, args[0].color, args[0].historic_positions)

	# Retorna um array de posição onde o primeiro indice é uma posição valida para se movimentar e o segundo indice uma peça inimiga que pode ser atacada.
	def availablePositions(self, table):
		return_possibilities = []

		for sum_y in (-1, 0, 1):
			for sum_x in (-1, 0, 1):
				if sum_x == 0 and sum_y == 0:
					continue
				new_position = self.actualPosition()
				count = 0
				other_piece = None
				while Piece.validPosition(new_position) and other_piece == None:
					if count != 0:
						return_possibilities.append([new_position, other_piece, None])
					count = count + 1
					new_position = (new_position[0] + sum_x, new_position[1] + sum_y)
					other_piece = table.findPiece(new_position)

				if other_piece != None and other_piece.color != self.color:
					return_possibilities.append([new_position, other_piece, None])

		return return_possibilities