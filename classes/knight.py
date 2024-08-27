from classes.piece import Piece

class Knight(Piece):
	def __init__(self, *args):
		self.points = 5
		if len(args) == 2:
			self.image_file = './assets/' + args[0] + 'Knight.png'
			super().__init__(self.image_file, args[0], args[1])
		elif len(args) == 1:
			self.image_file = './assets/' + args[0].color + 'Knight.png'
			super().__init__(self.image_file, args[0].color, args[0].historic_positions)

	def availablePositions(self, table):
		return_possibilities = []

		for sum_y in (-2, 2):
			for sum_x in (-1, 1):
				new_position = (self.actualPosition()[0] + sum_x, self.actualPosition()[1] + sum_y)
				other_piece = table.findPiece(new_position)
				if Piece.validPosition(new_position):
					if other_piece == None:
						return_possibilities.append([new_position, other_piece, None])
					elif other_piece.color != self.color:
						return_possibilities.append([new_position, other_piece, None])

		for sum_x in (-2, 2):
			for sum_y in (-1, 1):
				new_position = (self.actualPosition()[0] + sum_x, self.actualPosition()[1] + sum_y)
				other_piece = table.findPiece(new_position)
				if Piece.validPosition(new_position):
					if other_piece == None:
						return_possibilities.append([new_position, other_piece, None])
					elif other_piece.color != self.color:
						return_possibilities.append([new_position, other_piece, None])

		return return_possibilities