from PPlay import mouse
from PPlay.sprite import Sprite
from classes.front_menu import initialMenu

FRAME_RATE = 0.8
mouse = mouse.Mouse()

def menu(janela, front, table):
  delta_accumulator = 0.0
  initialMenu(janela)

  white_piece_allow = Sprite("./assets/white_piece_allow.png")
  white_piece_unable = Sprite("./assets/white_piece_unable.png")
  black_piece_allow = Sprite("./assets/black_piece_allow.png")
  black_piece_unable = Sprite("./assets/black_piece_unable.png")

  play_button = Sprite("./assets/play_button.png")

  white_piece_allow.set_position(846, 250)
  white_piece_unable.set_position(846, 250)
  black_piece_allow.set_position(1006, 250)
  black_piece_unable.set_position(1006, 250)

  play_button.set_position(846, 554)

  white_piece_allow.draw()
  black_piece_unable.draw()
  play_button.draw()

  players = [False, True]

  while 1:
    front.printTable(table)
    delta_accumulator += janela.delta_time() * 6

    if (mouse.is_over_object(white_piece_allow) and mouse.is_button_pressed(1) and (delta_accumulator > FRAME_RATE)):
      delta_accumulator = 0.0
      if not players[0]:
        players[0] = True
        white_piece_unable.draw()
      else:
        players[0] = False
        white_piece_allow.draw()

    if (mouse.is_over_object(black_piece_unable) and mouse.is_button_pressed(1) and (delta_accumulator > FRAME_RATE)):
      delta_accumulator = 0.0
      if not players[1]:
        players[1] = True
        black_piece_unable.draw()
      else:
        players[1] = False
        black_piece_allow.draw()

    if (mouse.is_over_object(play_button) and mouse.is_button_pressed(1)):
      break

    janela.update()


  janela.clear()
  return players