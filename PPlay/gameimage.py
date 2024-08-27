import sys
import pygame
from pygame.locals import *
from . import window
from . import gameobject

pygame.init()

def load_image(name, colorkey=None, alpha=False):
    image = pygame.image.load(name)
    # Se alpha for True, a imagem será convertida para alpha, senão, será convertida para 24 bits
    if alpha:image = image.convert_alpha()
    else:image=image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

# Criando a classe GameImage
class GameImage(gameobject.GameObject):

    def __init__(self, image_file):
        gameobject.GameObject.__init__(self)
        
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.width = self.rect.width
        self.height = self.rect.height

    def draw(self):
        
        # Atualizando a posição da imagem na tela
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        window.Window.get_screen().blit(self.image, self.rect)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def collided_perfect(self, target):
        from . import collision

        return collision.Collision.collided_perfect(self, target)