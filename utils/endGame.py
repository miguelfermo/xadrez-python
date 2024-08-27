from utils.prettyOutput import *

def endGame(result, winner=''):
  if result == 0:
    with prettyOutput(FG_CYAN) as out:
      out.write('Jogo finalizado por empate!')
  else:
    if winner.system_controlled == True:
      with prettyOutput(FG_RED) as out:
        out.write('Xeque mate! Vitória de ' + winner.name + "(" + winner.color + ")")
    else:
      with prettyOutput(FG_GREEN) as out:
        out.write('Xeque mate! Vitória de ' + winner.name + "(" + winner.color + ")")