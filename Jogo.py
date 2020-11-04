import pygame
import time
import random
import sys
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import Cena

class Jogo:
    def __init__(self, cena, janela, mouse):
        self.cena = cena
        self.mouse = mouse
        self.window = janela

        #definir Imagens e Sprites
        self.bggame = GameImage('sprites/bg-game.png')
        self.casaclara = Sprite('sprites/sprite-casa-clara.png')
        self.casaescura = Sprite('sprites/sprite-casa-escura.png')
        self.peaob = Sprite('sprites/sprite-peao-branco.png')
        self.peaop = Sprite('sprites/sprite-peao-preto.png')
        self.damab = Sprite('sprites/sprite-dama-branco.png')
        self.damap = Sprite('sprites/sprite-dama-preto.png')
        self.selecionada = Sprite('sprites/sprite-casa-selecionada.png')
        self.liberada = Sprite('sprites/sprite-casa-liberada.png')

        #auxiliares para posicionamento de desenho
        self.xini = 186.5
        self.yini = 0
        self.tamcasa = 60

        self.turno = 1
        self.jogadores = ('x', 'o')
        self.casa_selecionada = None
        self.lista_possibilidades = None
        self.pulando = 0
        
        #criar tabuleiro
        self.tabuleirodes = []

        #definir posicoes iniciais
        self.posx = self.xini
        self.posy = self.yini

        #variavel auxiliar de controle de cor da casa
        self.contcor = 1
        self.contlinha = 1
        #"povoar" tabuleiro para desenho
        for i in range(8):
            #criar linha
            linha = [] # lista vazia
            #definir cor da primeira casa (1 escuro, 0 clara)
            if (i % 2 == 0):
                self.contcor = 0
            else:
                self.contcor = 1
            #loop interno
            for j in range(8):
                if(self.contcor) == 1:
                    casa = Sprite('sprites/sprite-casa-escura.png')
                    casa.x = self.posx
                    casa.y = self.posy
                    linha.append(casa)
                    self.contcor = 0
                else:
                    casa = Sprite('sprites/sprite-casa-clara.png')
                    casa.x = self.posx
                    casa.y = self.posy
                    linha.append(casa)
                    self.contcor = 1
                #atualizar valor da pos x
                self.posx = self.posx + self.tamcasa
            #inserir linha na matriz
            self.tabuleirodes.append(linha)
            #redefinir o X para Xini
            self.posx = self.xini
            #atualizar o y para prox linha
            self.posy = self.posy + self.tamcasa
            #atualizar linha
            self.contlinha = self.contlinha + 1

        #tabuleiro de jogo
        self.tabuleiro = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                          ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
                          ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', 'o', '-', 'o', '-', 'o', '-', 'o'],
                          ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
                          ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]

    def desenhatabuleiro(self):
        if(self.casa_selecionada):
            self.lista_possibilidades = self.verificarjogadas()
        for linha in self.tabuleirodes:
            for casa in linha:
                casa.draw()
                if (self.lista_possibilidades != None):
                    for elemento in self.lista_possibilidades:
                        if (elemento == casa):
                            self.liberada.x = casa.x;
                            self.liberada.y = casa.y;
                            self.liberada.draw()
                if(self.casa_selecionada == casa):
                    self.selecionada.x = casa.x
                    self.selecionada.y = casa.y
                    self.selecionada.draw()

    
    def desenhajogo(self):
        #definir posições iniciais
        self.peaob.x = self.xini
        self.peaob.y = self.yini
        self.peaop.x = self.xini
        self.peaop.y = self.yini
        #variavel auxiliar de controle de cor da casa
        self.contcor = 1
        self.contlinha = 1
        #iniciar loop
        for linha in self.tabuleiro:
            if (self.contlinha % 2 == 0):
                self.contcor = 0
            else:
                self.contcor = 1
            #loop interno
            for casa in linha:
                if(casa == 'x'):
                    self.peaop.draw()
                elif(casa == 'o'):
                    self.peaob.draw()
                self.peaob.x = self.peaob.x + self.tamcasa
                self.peaop.x = self.peaop.x + self.tamcasa
            #redefinir o X para Xini
            self.peaob.x = self.xini
            self.peaop.x = self.xini
            #atualizar o y para prox linha
            self.peaob.y = self.peaob.y + self.tamcasa
            self.peaop.y = self.peaop.y + self.tamcasa
            #atualizar linha
            self.contlinha = self.contlinha + 1

    #função que define célula selecionada
    def selecionar(self):
        pos = self.mouse.get_position()
        for linha in self.tabuleirodes:
            for casa in linha:
                if ((casa.x < pos[0]) and ((casa.x + self.tamcasa) > pos[0]) and (casa.y < pos[1]) and (
                        (casa.y + self.tamcasa) > pos[1])):
                    self.casa_selecionada = casa
        return None

    def verificarjogadas(self):
        #lista de marcadas
        if(self.casa_selecionada):
            possibilidades = []
            #localizar posição da celula celecionada e verificar de acordo com o tipo de peça se há jogadas disponiveis
            for i in range (8):
                for j in range (8):
                    if(self.tabuleirodes[i][j] == self.casa_selecionada):
                        if (self.tabuleiro[i][j] == self.jogadores[0]):
                            #verifica casas diagonais abaixo
                            if((j-1)>0 and self.tabuleiro[i+1][j-1]=='-'):
                                possibilidades.append(self.tabuleirodes[i+1][j-1])
                            if((j+1)<8 and self.tabuleiro[i+1][j+1]=='-'):
                                possibilidades.append(self.tabuleirodes[i+1][j+1])
                        elif(self.tabuleiro[i][j] == self.jogadores[1]):
                            # verifica casas diagonais acima
                            if ((j-1)>0 and self.tabuleiro[i - 1][j - 1] == '-'):
                                possibilidades.append(self.tabuleirodes[i - 1][j - 1])
                            if ((j+1)<8 and self.tabuleiro[i - 1][j + 1] == '-'):
                                possibilidades.append(self.tabuleirodes[i - 1][j + 1])
            # a lista de casas possiveis
            return possibilidades
        return None

    def jogo(self):
        #desenhar tabuleiro
        self.bggame.draw()
        self.desenhatabuleiro()
        self.desenhajogo()
        #Verificar Clique no mouse e fazer seleção
        if (self.mouse.is_button_pressed(1)):
            self.selecionar()

