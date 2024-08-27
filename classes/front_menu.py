import pdb
from PPlay.sprite import Sprite

def initialMenu(janela):
  janela.set_title('Xadrez')
  janela.draw_text("XADREZ", 889, 11, size=48, color=(0,0,0), font_name="Arial", bold=False, italic=False)
  janela.draw_text("Menu Principal", 913, 115, size=18, color=(0,0,0), font_name="Arial", bold=False, italic=False)

def mainMenu(janela, can_revert):
  if can_revert:
    revert_button = Sprite("./assets/revert_button.png")
    revert_button.set_position(846, 258)
    revert_button.draw()

  janela.draw_text("XADREZ", 889, 11, size=48, color=(0,0,0), font_name="Arial", bold=False, italic=False)
  janela.draw_text("Vez de:", 774, 87, size=18, color=(0,0,0), font_name="Arial", bold=False, italic=False)

  restart_button = Sprite("./assets/restart_button.png")
  restart_button.set_position(846, 333)
  restart_button.draw()

  # janela.update()

def white_time_to_play():
  white_time_to_play = Sprite("./assets/white_time_to_play.png")
  white_time_to_play.set_position(870, 127)
  white_time_to_play.draw()

  black_no_time_to_play = Sprite("./assets/black_no_time_to_play.png")
  black_no_time_to_play.set_position(1010, 127)
  black_no_time_to_play.draw()

def black_time_to_play():
  white_no_time_to_play = Sprite("./assets/white_no_time_to_play.png")
  white_no_time_to_play.set_position(870, 127)
  white_no_time_to_play.draw()

  black_time_to_play = Sprite("./assets/black_time_to_play.png")
  black_time_to_play.set_position(1010, 127)
  black_time_to_play.draw()

def promoteFront(janela, front): 
  janela.draw_text("PROMOVER PARA", 749, 448, size=24, color=(0,0,0), font_name="Arial", bold=False, italic=False)

  selected = None
  while selected == None:
    queen_button = Sprite("./assets/queen_button.png")
    queen_button.set_position(758, 491)
    queen_button.draw()

    rook_button = Sprite("./assets/rook_button.png")
    rook_button.set_position(879, 491)
    rook_button.draw()

    bishop_button = Sprite("./assets/bishop_button.png")
    bishop_button.set_position(1000, 491)
    bishop_button.draw()

    knight_button = Sprite("./assets/knight_button.png")
    knight_button.set_position(1121, 491)
    knight_button.draw()

    mouse_entry = front.mouseReader(janela)
    if mouse_entry:
      if 758 < mouse_entry[0] < 858 and 491 < mouse_entry[1] < 591:
        return 0
      if 879 < mouse_entry[0] < 979 and 491 < mouse_entry[1] < 591:
        return 1
      if 1000 < mouse_entry[0] < 1100 and 491 < mouse_entry[1] < 591:
        return 2
      if 1121 < mouse_entry[0] < 1221 and 491 < mouse_entry[1] < 591:
        return 3