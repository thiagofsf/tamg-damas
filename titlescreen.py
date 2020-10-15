import pygame
import time
import random
import sys
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *

#tela Inicial
bgini = GameImage('sprites/bg-title.png')

titlelogo = Sprite('sprites/title-logo.png')
titlelogo.x = 0
titlelogo.y = 0

startgame = Sprite('sprites/btn-novojogo.png')
startgame.x = window.width/2 - startgame.width/2
startgame.y = 300
startgameover = Sprite('sprites/btn-novojogo-over.png')
startgameover.x = window.width/2 - startgame.width/2
startgameover.y = 300

tamglogo = Sprite('sprites/btn-tamg.png')
tamglogo.x = window.width - tamglogo.width - 10
tamglogo.y = window.height - tamglogo.height - 10
tamglogoover = Sprite('sprites/btn-tamg-over.png')
tamglogoover.x = window.width - tamglogo.width - 10
tamglogoover.y = window.height - tamglogo.height - 10

def telaTitulo():
    global SCENE

    bgini.draw()
    titlelogo.draw()

    #desenhar o botão novo jogo de acordo com a pos do mouse
    if mouse.is_over_object(startgame):
        startgameover.draw()
    else:
        startgame.draw()
    #desenhar o botao com logo tamg de acordo com a pos do mouse
    if mouse.is_over_object(tamglogo):
        tamglogoover.draw()
    else:
        tamglogo.draw()

    #testar se o usuario clicou e mudar a SCENE
    if mouse.is_over_object(startgame) and mouse.is_button_pressed(1):
        SCENE = 'game'
        window.delay(300)
    if mouse.is_over_object(tamglogo) and mouse.is_button_pressed(1):
        SCENE = 'about'
        window.delay(300)
    return None