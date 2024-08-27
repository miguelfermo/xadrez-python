import sys
import pygame
from pygame.locals import *
from . import keyboard
from . import mouse

# Inicializando pygame
pygame.init()

# Iniciando classe Window
class Window():
	
	screen = None

	# --------------------- CONSTRUCTOR --------------------------- #
	def __init__(self, width, height):
		# Input control
		Window.keyboard = keyboard.Keyboard()
		Window.mouse = mouse.Mouse()

		# Tamanhos de tela
		self.width = width
		self.height = height

		self.color = [0,0,0]  # Preto
		self.title = "Xadrez"

		# Time Control
		self.curr_time = 0  # current frame time
		self.last_time = 0  # last frame time
		self.total_time = 0  # += curr-last(delta_time), update()

		# Criando a tela
		Window.screen = pygame.display.set_mode([self.width, self.height])

		# Setando as propriedades iniciais
		self.set_background_color(self.color)
		self.set_title(self.title)

		pygame.display.update()

	# ----------------------- CONTROL METHODS --------------------------- #
	def update(self):
		pygame.display.update()  # refresh na pagina

		for event in pygame.event.get():  # caso feche a janela, pare o programa
			if event.type==QUIT:
				self.close()
		self.last_time = self.curr_time  
		self.curr_time = pygame.time.get_ticks()  
		self.total_time += (self.curr_time - self.last_time) 

	def clear(self):
		self.set_background_color([255,255,255])
		self.update()


	def close(self):
		pygame.quit()
		sys.exit()

	# ------------------------ GETTERS AND SETTERS --------------------- #

	# Seta a cor de fundo da janela
	def set_background_color(self, RGB):
		self.color = RGB
		Window.screen.fill(self.color)

	# Retorna a cor de fundo da janela
	def get_background_color(self):
		return self.color

	# Seta o título da janela
	def set_title(self, title):
		self.title = title
		pygame.display.set_caption(title)

	# Retorna o título da janela
	def get_title(self):
		return self.title

	#----------------------TIME CONTROL METHODS--------------------------

	# Pode ser usado para controlar a velocidade do jogo, dando um delay
	def delay(self, time_ms):
		pygame.time.delay(time_ms)

	# Retorna o tempo passado entre o último e o atual frame - SEGUNDOS
	def delta_time(self):
		return (self.curr_time - self.last_time)/1000.0

	# Retorna o tempo total passado desde que a janela foi criada
	def time_elapsed(self):
		return self.total_time

	#------------------------DRAW METHODS-------------------------------

	# Essa função desenha um texto na tela nas coordenadas X e Y, usando a cor [R, G, B]
	def draw_text(self, text, x, y, size=12, color=(0,0,0),
	              font_name="Arial", bold=False, italic=False):
		
		font = pygame.font.SysFont(font_name, size, bold, italic)

		# Criando uma superfície com o texto renderizado
		font_surface = font.render(text, True, color)

		# Desenha a superfície na tela
		self.screen.blit(font_surface, [x, y])

	#---------------------CLASS METHODS--------------------------

	# Retorna a tela
	@classmethod
	def get_screen(cls):
		return cls.screen

	# Retorna o teclado
	@classmethod
	def get_keyboard(cls):
		return cls.keyboard

	# Retorna o mouse
	@classmethod
	def get_mouse(cls):
		return cls.mouse
    
# ==================================================================================================== #
# ==================================================================================================== #