import pygame
import time
import random
import sys
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import Cena

class TelaDerrota:
    def __init__(self, cena, janela, mouse):

        self.cena = cena
        self.window = janela
        self.mouse = mouse

        self.sobrebg = GameImage('sprites/bg-lose.png')

        self.back = Sprite('sprites/btn-inicio.png')
        self.back.x = self.window.width/2 - self.back.width/2
        self.back.y = 400
        self.backover = Sprite('sprites/btn-inicio-over.png')
        self.backover.x = self.window.width/2 - self.backover.width/2
        self.backover.y = 400

    def derrota(self):
        self.sobrebg.draw()
        # desenhar o botão de retorno de acordo com a pos do mouse
        if self.mouse.is_over_object(self.back):
            self.backover.draw()
        else:
            self.back.draw()

        # testar se o usuario clicou em voltar e mudar a SCENE
        if self.mouse.is_over_object(self.back) and self.mouse.is_button_pressed(1):
            self.cena.setCena('title')
            self.window.delay(300)
        return None
