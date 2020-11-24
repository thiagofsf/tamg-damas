import pygame
import time
import random
import sys
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from TelaTitulo import *
from TelaSobre import *
from Jogo import *
from TelaVitoria import *
from TelaDerrota import *
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

#novo jogo
telajogo = Jogo(cena, window, mouse)

#nova tela de Vitoria
telavitoria = TelaVitoria(cena, window, mouse)

#nova tela de Derrota
teladerrota = TelaDerrota(cena, window, mouse)

####### GAME LOOP ########
while True:
    if cena.getCena() == 'title':
        telatitulo.telaTitulo()
    elif cena.getCena() == 'about':
        telasobre.sobre()
    elif cena.getCena() == 'game':
        telajogo.jogo()
    elif cena.getCena() == 'win':
        telavitoria.vitoria()
    elif cena.getCena() == 'lose':
        teladerrota.derrota()
    window.update()