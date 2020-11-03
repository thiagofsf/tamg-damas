import pygame
import time
import random
import sys
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from TelaTitulo import *
from TelaSobre import *
from Cena import *

#definir janela
window = Window(853,480)
window.set_title("Tamg Damas")

#carregar inputs
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

#variavel de controle de cenas
cena =Cena('title')

#nova tela de titulo
telatitulo = TelaTitulo(cena, window, mouse)

#nova tela de Sobre
telasobre = TelaSobre(cena, window, mouse)

#Procedimento de jogo
gamebg = GameImage('sprites/bg-board.png')
def game():
    gamebg.draw()
    return None

####### GAME LOOP ########
while True:
    if cena.getCena() == 'title':
        telatitulo.telaTitulo()
    elif cena.getCena() == 'about':
        telasobre.sobre()
    elif cena.getCena() == 'game':
        game()
    window.update()