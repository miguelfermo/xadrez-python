from . import point
import pygame

# Ta curioso mesmo, veio ver o código fonte até aqui?
class Collision():

    @classmethod
    def collided_rect(cls, min1, max1, min2, max2):
        if(min1.x >= max2.x or max1.x <= min2.x):
            return False
        if(min1.y >= max2.y or max1.y <= min2.y):
            return False
        return True

    @classmethod
    def collided(cls, *args):

        game_object1_min = point.Point(args[0].x, args[0].y)
        game_object1_max = point.Point(args[0].x + args[0].width,
                                 args[0].y + args[0].height)

        game_object2_min = point.Point(args[1].x, args[1].y)
        game_object2_max = point.Point(args[1].x + args[1].width,
                                 args[1].y + args[1].height)

        return (Collision.collided_rect(game_object1_min, game_object1_max,
                                        game_object2_min, game_object2_max))

    @classmethod
    def perfect_collision(cls, gameimage1, gameimage2):

        offset_x = (gameimage2.rect.left - gameimage1.rect.left)
        offset_y = (gameimage2.rect.top - gameimage1.rect.top)
        
        mask_1 = pygame.mask.from_surface(gameimage1.image)
        mask_2 = pygame.mask.from_surface(gameimage2.image)
        
        if(mask_1.overlap(mask_2, (offset_x, offset_y)) != None):
            return True
        return False


    @classmethod
    def collided_perfect(cls, gameimage1, gameimage2):
        return (Collision.perfect_collision(gameimage1, gameimage2))