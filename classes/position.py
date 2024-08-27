from PPlay.sprite import Sprite


class Position(Sprite):
	def __init__(self, color, position):
		image_file = './assets/' + color + 'Position.jpg'
		super().__init__(image_file)
		self.position = position
		self.color = color

		# Cada casa terá um círculo localizado no meio
		# que só será desenhado quando aquela casa for uma opção de movimento
		self.circle = Sprite('assets/circle.png')
		self.attack_circle = Sprite('assets/crosshair.png')
		self.isCircleOn = False
		self.isUnderAttack = False

		# Cada casa terá uma borda locaizada na mesma posição da casa
		# que só será desenhado quando o mouse estiver sobre aquela casa
		self.border = Sprite('assets/borda_marrom.png')
		self.isBorderOn = False
