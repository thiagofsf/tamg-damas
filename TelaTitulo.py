import pygame
import time
import random
import sys
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import Cena

class TelaTitulo:

    def __init__(self, cena, janela, mouse):

        self.cena = cena
        self.mouse = mouse
        self.janela = janela

        self.bgini = GameImage('sprites/bg-title.png')

        self.titlelogo = Sprite('sprites/title-logo.png')
        self.titlelogo.x = 0
        self.titlelogo.y = 0

        self.startgame = Sprite('sprites/btn-novojogo.png')
        self.startgame.x = janela.width / 2 - self.startgame.width / 2
        self.startgame.y = 300
        self.startgameover = Sprite('sprites/btn-novojogo-over.png')
        self.startgameover.x = janela.width / 2 - self.startgame.width / 2
        self.startgameover.y = 300

        self.tamglogo = Sprite('sprites/btn-tamg.png')
        self.tamglogo.x = janela.width - self.tamglogo.width - 10
        self.tamglogo.y = janela.height - self.tamglogo.height - 10
        self.tamglogoover = Sprite('sprites/btn-tamg-over.png')
        self.tamglogoover.x = janela.width - self.tamglogo.width - 10
        self.tamglogoover.y = janela.height - self.tamglogo.height - 10

    def telaTitulo(self):

        self.bgini.draw()
        self.titlelogo.draw()

        #desenhar o botão novo jogo de acordo com a pos do mouse
        if self.mouse.is_over_object(self.startgame):
            self.startgameover.draw()
        else:
            self.startgame.draw()
        #desenhar o botao com logo tamg de acordo com a pos do mouse
        if self.mouse.is_over_object(self.tamglogo):
            self.tamglogoover.draw()
        else:
            self.tamglogo.draw()

        #testar se o usuario clicou e mudar a SCENE
        if self.mouse.is_over_object(self.startgame) and self.mouse.is_button_pressed(1):
            self.cena.setCena('game')
            self.janela.delay(300)
        if self.mouse.is_over_object(self.tamglogo) and self.mouse.is_button_pressed(1):
            self.cena.setCena('about')
            self.janela.delay(300)
        return None