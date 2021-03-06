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
        self.atraso = 0

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
        self.xini = 186
        self.yini = 0
        self.tamcasa = 60

        self.turno = 1
        self.jogadores = ('x', 'o')
        self.casa_selecionada = None
        self.lista_possibilidades = None
        self.lista_obrigatorias = None
        self.pecapulo = None
        self.pulo = 0
        self.continuapulo = 0
        
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

        #uso em testes
        self.tabuleirot = [['x', '-', 'x', '-', 'o', '-', 'x', '-'],
                          ['-', 'x', '-', 'x', '-', '-', '-', 'x'],
                          ['x', '-', 'x', '-', '-', '-', 'x', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', 'x', '-'],
                          ['-', 'o', '-', '-', '-', '-', '-', 'o'],
                          ['o', '-', 'o', '-', 'x', '-', 'o', '-'],
                          ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]

    def desenhatabuleiro(self):
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
        self.damab.x = self.xini
        self.damab.y = self.yini
        self.damap.x = self.xini
        self.damap.y = self.yini
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
                elif(casa == 'X'):
                    self.damap.draw()
                elif(casa == 'o'):
                    self.peaob.draw()
                elif(casa == 'O'):
                    self.damab.draw()
                self.peaob.x = self.peaob.x + self.tamcasa
                self.peaop.x = self.peaop.x + self.tamcasa
                self.damab.x = self.damab.x + self.tamcasa
                self.damap.x = self.damap.x + self.tamcasa
            #redefinir o X para Xini
            self.peaob.x = self.xini
            self.peaop.x = self.xini
            self.damab.x = self.xini
            self.damap.x = self.xini
            #atualizar o y para prox linha
            self.peaob.y = self.peaob.y + self.tamcasa
            self.peaop.y = self.peaop.y + self.tamcasa
            self.damab.y = self.damab.y + self.tamcasa
            self.damap.y = self.damap.y + self.tamcasa
            #atualizar linha
            self.contlinha = self.contlinha + 1

    #verifica dama
    def verificaDama(self):
        for i in range(8):
            if(self.tabuleiro[0][i] == 'o'):
                self.tabuleiro[0][i] = 'O'
        for i in range(8):
            if(self.tabuleiro[7][i] == 'x'):
                self.tabuleiro[7][i] = 'X'
        return None

    #função que define célula selecionada
    def selecionar(self):
        pos = self.mouse.get_position()
        if(self.lista_obrigatorias == None):
            for linha in self.tabuleirodes:
                for casa in linha:
                    if ((casa.x < pos[0]) and ((casa.x + self.tamcasa) > pos[0]) and (casa.y < pos[1]) and (
                            (casa.y + self.tamcasa) > pos[1])):
                        self.casa_selecionada = casa
        else:
            for elemento in self.lista_obrigatorias:
                if ((elemento.x < pos[0]) and ((elemento.x + self.tamcasa) > pos[0]) and (elemento.y < pos[1]) and (
                        (elemento.y + self.tamcasa) > pos[1])):
                    self.casa_selecionada = elemento
        #self.atraso = 1
        return None

    #peça 1: representação do peao, peça 2: representação da dama (a função deve ser adaptada para cada turno) funciona apenas para o jogador
    def verificarsehajogadaspossiveis(self, peca1, peca2):
        possibilidades = []
        # pra cada celula
        for i in range(8):
            for j in range(8):
                if (self.tabuleiro[i][j] == peca1):
                    # verifica casas diagonais acima (jogador apenas pode mover para cima
                    if ((j - 1) >= 0 and self.tabuleiro[i - 1][j - 1] == '-'):
                        possibilidades.append(self.tabuleirodes[i - 1][j - 1])
                    if ((j + 1) < 8 and self.tabuleiro[i - 1][j + 1] == '-'):
                        possibilidades.append(self.tabuleirodes[i - 1][j + 1])
                elif (self.tabuleiro[i][j] == peca2):
                    tempi = i - 1
                    tempj = j - 1
                    while (tempi >= 0 and tempj >= 0):
                        if (self.tabuleiro[tempi][tempj] == '-'):
                            possibilidades.append(self.tabuleirodes[tempi][tempj])
                        else:
                            break
                        tempi = tempi - 1
                        tempj = tempj - 1
                    tempi = i - 1
                    tempj = j + 1
                    while (tempi >= 0 and tempj < 8):
                        if (self.tabuleiro[tempi][tempj] == '-'):
                            possibilidades.append(self.tabuleirodes[tempi][tempj])
                        else:
                            break
                        tempi = tempi - 1
                        tempj = tempj + 1
                    tempi = i + 1
                    tempj = j - 1
                    while (tempi < 8 and tempj >= 0):
                        if (self.tabuleiro[tempi][tempj] == '-'):
                            possibilidades.append(self.tabuleirodes[tempi][tempj])
                        else:
                            break
                        tempi = tempi + 1
                        tempj = tempj - 1
                    tempi = i + 1
                    tempj = j + 1
                    while (tempi < 8 and tempj < 8):
                        if (self.tabuleiro[tempi][tempj] == '-'):
                            possibilidades.append(self.tabuleirodes[tempi][tempj])
                        else:
                            break
                        tempi = tempi + 1
                        tempj = tempj + 1
        # a lista de casas possiveis
        if(possibilidades!= []):
            return 1
        return 0

    def verificarjogadas(self):
        #lista de marcadas
        if(self.casa_selecionada):
            possibilidades = []
            if(self.lista_obrigatorias):
                for i in range(8):
                    for j in range(8):
                        if (self.tabuleirodes[i][j] == self.casa_selecionada):
                            if(self.tabuleiro[i][j] == 'x'):
                                # se casas diagonais abaixo:
                                if (i + 1 < 8 and i + 2 < 8):
                                    # se a casa diagonal existe e tem peça oponente:
                                    if ((j - 1) >= 0 and (self.tabuleiro[i + 1][j - 1] == 'o' or self.tabuleiro[i + 1][j - 1] == 'O')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j - 2) >= 0 and self.tabuleiro[i + 2][j - 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i+2][j-2])
                                            self.pulo = 1
                                    # se a outra diagonal existe e tem peça oponente:
                                    if ((j + 1) < 8 and (self.tabuleiro[i + 1][j + 1] == 'o' or self.tabuleiro[i + 1][j + 1] == 'O')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j + 2) < 8 and self.tabuleiro[i + 2][j + 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i + 2][j + 2])
                                            self.pulo = 1
                                #verificar casas diagonais acima
                                if(i - 1 >= 0 and i - 2 >= 0):
                                    # se a casa diagonal existe e tem peça oponente:
                                    if ((j - 1) >= 0 and (self.tabuleiro[i - 1][j - 1] == 'o' or self.tabuleiro[i - 1][j - 1] == 'O')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j - 2) >= 0 and self.tabuleiro[i - 2][j - 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i - 2][j - 2])
                                            self.pulo = 1
                                    # se a outra diagonal existe e tem peça oponente:
                                    if ((j + 1) < 8 and (self.tabuleiro[i - 1][j + 1] == 'o' or self.tabuleiro[i - 1][j + 1] == 'O')):
                                        # verifica se existe casa vazia nmesa ma diagonal
                                        if ((j + 2) < 8 and self.tabuleiro[i - 2][j + 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i - 2][j + 2])
                                            self.pulo = 1
                            #se houver obrigatoria e Dama
                            elif (self.tabuleiro[i][j] == 'X'):
                                tempi = i
                                tempj = j
                                continuarappend = 0
                                while (tempi >= 0 and tempj >= 0):
                                    if (continuarappend == 0 and tempi - 1 >= 0 and tempj - 1 >= 0 and tempi - 2 >= 0 and tempj - 2 >= 0):
                                        if (self.tabuleiro[tempi - 1][tempj - 1] == 'o' or self.tabuleiro[tempi - 1][tempj - 1] == 'O'):
                                            if (self.tabuleiro[tempi - 2][tempj - 2] == '-'):
                                                possibilidades.append(self.tabuleirodes[tempi - 2][tempj - 2])
                                                tempi = tempi - 2
                                                tempj = tempj - 2
                                                continuarappend = 1
                                                self.pulo = 1
                                            elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                                break
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] != '-'):
                                        break
                                    tempi = tempi - 1
                                    tempj = tempj - 1
                                tempi = i
                                tempj = j
                                continuarappend = 0
                                while (tempi >= 0 and tempj < 8):
                                    if (continuarappend == 0 and (tempi - 1 >= 0) and (tempj + 1 < 8) and (tempi - 2 >= 0) and (tempj + 2 < 8)):
                                        if (self.tabuleiro[tempi - 1][tempj + 1] == 'o' or self.tabuleiro[tempi - 1][tempj + 1] == 'O'):
                                            if (self.tabuleiro[tempi - 2][tempj + 2] == '-'):
                                                possibilidades.append(self.tabuleirodes[tempi - 2][tempj + 2])
                                                tempi = tempi - 2
                                                tempj = tempj + 2
                                                continuarappend = 1
                                                self.pulo = 1
                                            elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                                break
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] != '-'):
                                        break
                                    tempi = tempi - 1
                                    tempj = tempj + 1
                                tempi = i
                                tempj = j
                                continuarappend = 0
                                while (tempi < 8 and tempj >= 0):
                                    if (continuarappend == 0 and (tempi + 1 < 8) and (tempj - 1 >= 0) and (tempi + 2 < 8) and (tempj - 2 >= 0)):
                                        if (self.tabuleiro[tempi + 1][tempj - 1] == 'o' or self.tabuleiro[tempi + 1][tempj - 1] == 'O'):
                                            if (self.tabuleiro[tempi + 2][tempj - 2] == '-'):
                                                possibilidades.append(self.tabuleirodes[tempi + 2][tempj - 2])
                                                tempi = tempi + 2
                                                tempj = tempj - 2
                                                continuarappend = 1
                                                self.pulo = 1
                                            elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                                break
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] != '-'):
                                        break
                                    tempi = tempi + 1
                                    tempj = tempj - 1
                                tempi = i
                                tempj = j
                                continuarappend = 0
                                while (tempi < 8 and tempj < 8):
                                    if (continuarappend == 0 and (tempi + 1 < 8) and (tempj + 1 < 8) and (tempi + 2 < 8) and (tempj + 2 < 8)):
                                        if (self.tabuleiro[tempi + 1][tempj + 1] == 'o' or self.tabuleiro[tempi + 1][tempj + 1] == 'O'):
                                            if (self.tabuleiro[tempi + 2][tempj + 2] == '-'):
                                                possibilidades.append(self.tabuleirodes[tempi + 2][tempj + 2])
                                                tempi = tempi + 2
                                                tempj = tempj + 2
                                                continuarappend = 1
                                                self.pulo = 1
                                            elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                                break
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] != '-'):
                                        break
                                    tempi = tempi + 1
                                    tempj = tempj + 1
                            elif(self.tabuleiro[i][j] == 'o'):
                                # se casas diagonais abaixo:
                                if (i + 1 < 8 and i + 2 < 8):
                                    # se a casa diagonal existe e tem peça oponente:
                                    if ((j - 1) >= 0 and (self.tabuleiro[i + 1][j - 1] == 'x' or self.tabuleiro[i + 1][j - 1] == 'X')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j - 2) >= 0 and self.tabuleiro[i + 2][j - 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i + 2][j - 2])
                                            self.pulo = 1
                                    # se a outra diagonal existe e tem peça oponente:
                                    if ((j + 1) < 8 and (self.tabuleiro[i + 1][j + 1] == 'x' or self.tabuleiro[i + 1][j + 1] == 'X')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j + 2) < 8 and self.tabuleiro[i + 2][j + 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i + 2][j + 2])
                                            self.pulo = 1
                                # verificar casas diagonais acima
                                if (i - 1 >= 0 and i - 2 >= 0):
                                    # se a casa diagonal existe e tem peça oponente:
                                    if ((j - 1) >= 0 and (self.tabuleiro[i - 1][j - 1] == 'x' or self.tabuleiro[i - 1][j - 1] == 'X')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j - 2) >= 0 and self.tabuleiro[i - 2][j - 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i - 2][j - 2])
                                            self.pulo = 1
                                    # se a outra diagonal existe e tem peça oponente:
                                    if ((j + 1) < 8 and (self.tabuleiro[i - 1][j + 1] == 'x' or self.tabuleiro[i - 1][j + 1] == 'X')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j + 2) < 8 and self.tabuleiro[i - 2][j + 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i - 2][j + 2])
                                            self.pulo = 1
                            elif(self.tabuleiro[i][j] == 'O'):
                                tempi = i
                                tempj = j
                                continuarappend = 0
                                while (tempi >= 0 and tempj >= 0):
                                    if (continuarappend == 0 and tempi - 1 >= 0 and tempj - 1 >= 0 and tempi - 2 >= 0 and tempj - 2 >= 0):
                                        if (self.tabuleiro[tempi - 1][tempj - 1] == 'x' or self.tabuleiro[tempi - 1][tempj - 1] == 'X'):
                                            if (self.tabuleiro[tempi - 2][tempj - 2] == '-'):
                                                possibilidades.append(self.tabuleirodes[tempi-2][tempj-2])
                                                tempi = tempi - 2
                                                tempj = tempj - 2
                                                continuarappend = 1
                                                self.pulo = 1
                                            elif(self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                                break
                                    elif(continuarappend == 1 and self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    elif(continuarappend == 1 and self.tabuleiro[tempi][tempj] != '-'):
                                        break
                                    tempi = tempi - 1
                                    tempj = tempj - 1
                                tempi = i
                                tempj = j
                                continuarappend = 0
                                while (tempi >= 0 and tempj < 8):
                                    if (continuarappend == 0 and (tempi - 1 >= 0) and (tempj + 1 < 8) and (tempi - 2 >= 0) and (tempj + 2 < 8)):
                                        if (self.tabuleiro[tempi - 1][tempj + 1] == 'x' or self.tabuleiro[tempi - 1][tempj + 1] == 'X'):
                                            if (self.tabuleiro[tempi - 2][tempj + 2] == '-'):
                                                possibilidades.append(self.tabuleirodes[tempi - 2][tempj+2])
                                                tempi = tempi - 2
                                                tempj = tempj + 2
                                                continuarappend = 1
                                                self.pulo = 1
                                            elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                                break
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] != '-'):
                                        break
                                    tempi = tempi - 1
                                    tempj = tempj + 1
                                tempi = i
                                tempj = j
                                continuarappend = 0
                                while (tempi < 8 and tempj >= 0):
                                    if (continuarappend == 0 and (tempi + 1 < 8) and (tempj - 1 >= 0) and (tempi + 2 < 8) and (tempj - 2 >= 0)):
                                        if (self.tabuleiro[tempi + 1][tempj - 1] == 'x' or self.tabuleiro[tempi + 1][tempj - 1] == 'X'):
                                            if (self.tabuleiro[tempi + 2][tempj - 2] == '-'):
                                                possibilidades.append(self.tabuleirodes[tempi + 2][tempj - 2])
                                                tempi = tempi + 2
                                                tempj = tempj - 2
                                                continuarappend = 1
                                                self.pulo = 1
                                            elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                                break
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] != '-'):
                                        break
                                    tempi = tempi + 1
                                    tempj = tempj - 1
                                tempi = i
                                tempj = j
                                continuarappend = 0
                                while (tempi < 8 and tempj < 8):
                                    if (continuarappend == 0 and (tempi + 1 < 8) and (tempj + 1 < 8) and (tempi + 2 < 8) and (tempj + 2 < 8)):
                                        if (self.tabuleiro[tempi + 1][tempj + 1] == 'x' or self.tabuleiro[tempi + 1][tempj + 1] == 'X'):
                                            if (self.tabuleiro[tempi + 2][tempj + 2] == '-'):
                                                possibilidades.append(self.tabuleirodes[tempi + 2][tempj + 2])
                                                tempi = tempi + 2
                                                tempj = tempj + 2
                                                continuarappend = 1
                                                self.pulo = 1
                                            elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                                break
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    elif (continuarappend == 1 and self.tabuleiro[tempi][tempj] != '-'):
                                        break
                                    tempi = tempi + 1
                                    tempj = tempj + 1
            else:
                #localizar posição da celula celecionada e verificar de acordo com o tipo de peça se há jogadas disponiveis
                for i in range (8):
                    for j in range (8):
                        if(self.tabuleirodes[i][j] == self.casa_selecionada):
                            if (self.tabuleiro[i][j] == 'x'):
                                #verifica casas diagonais abaixo
                                if((j-1)>=0 and self.tabuleiro[i+1][j-1]=='-'):
                                    possibilidades.append(self.tabuleirodes[i+1][j-1])
                                if((j+1)<8 and self.tabuleiro[i+1][j+1]=='-'):
                                    possibilidades.append(self.tabuleirodes[i+1][j+1])
                            elif (self.tabuleiro[i][j] == 'X'):
                                tempi = i - 1
                                tempj = j - 1
                                continuarappend = 0
                                while (tempi >= 0 and tempj >= 0):
                                    if(self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    else:
                                        break
                                    tempi = tempi - 1
                                    tempj = tempj - 1
                                tempi = i - 1
                                tempj = j + 1
                                continuarappend = 0
                                while (tempi >= 0 and tempj < 8):
                                    if (self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    else:
                                        break
                                    tempi = tempi - 1
                                    tempj = tempj + 1
                                tempi = i + 1
                                tempj = j - 1
                                continuarappend = 0
                                while (tempi < 8 and tempj >= 0):
                                    if (self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    else:
                                        break
                                    tempi = tempi + 1
                                    tempj = tempj - 1
                                tempi = i + 1
                                tempj = j + 1
                                continuarappend = 0
                                while (tempi < 8 and tempj < 8):
                                    if (self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    else:
                                        break
                                    tempi = tempi + 1
                                    tempj = tempj + 1
                            elif(self.tabuleiro[i][j] == 'o'):
                                # verifica casas diagonais acima
                                if ((j-1)>=0 and self.tabuleiro[i - 1][j - 1] == '-'):
                                    possibilidades.append(self.tabuleirodes[i - 1][j - 1])
                                if ((j+1)<8 and self.tabuleiro[i - 1][j + 1] == '-'):
                                    possibilidades.append(self.tabuleirodes[i - 1][j + 1])
                            elif (self.tabuleiro[i][j] == 'O'):
                                tempi = i - 1
                                tempj = j - 1
                                continuarappend = 0
                                while (tempi >= 0 and tempj >= 0):
                                    if(self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    else:
                                        break
                                    tempi = tempi - 1
                                    tempj = tempj - 1
                                tempi = i - 1
                                tempj = j + 1
                                continuarappend = 0
                                while (tempi >= 0 and tempj < 8):
                                    if (self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    else:
                                        break
                                    tempi = tempi - 1
                                    tempj = tempj + 1
                                tempi = i + 1
                                tempj = j - 1
                                continuarappend = 0
                                while (tempi < 8 and tempj >= 0):
                                    if (self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    else:
                                        break
                                    tempi = tempi + 1
                                    tempj = tempj - 1
                                tempi = i + 1
                                tempj = j + 1
                                continuarappend = 0
                                while (tempi < 8 and tempj < 8):
                                    if (self.tabuleiro[tempi][tempj] == '-'):
                                        possibilidades.append(self.tabuleirodes[tempi][tempj])
                                    else:
                                        break
                                    tempi = tempi + 1
                                    tempj = tempj + 1
            # a lista de casas possiveis
            return possibilidades
        return None

    def verificarObrigatorias(self):
        #lista de marcadas
        Obrigatorias = []
        if(self.turno == 0):
            for i in range (8):
                for j in range (8):
                    if(self.tabuleiro[i][j] == 'x'):
                        # se casas diagonais abaixo:
                        if(i+1<8 and i+2<8):
                            # se a diagonal existe e tem peça oponente:
                            if ((j - 1) >= 0 and (self.tabuleiro[i + 1][j - 1] == 'o' or self.tabuleiro[i + 1][j - 1] == 'O')):
                                # verifica se existe casa vazia na mesma diagonal
                                if ((j - 2) >= 0 and self.tabuleiro[i + 2][j - 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                            #se a outra diagonal existe e tem peça oponente:
                            if ((j + 1) < 8 and (self.tabuleiro[i + 1][j + 1] == 'o' or self.tabuleiro[i + 1][j + 1] == 'O')):
                                #verifica se existe casa vazia na mesma diagonal
                                if ((j + 2) < 8 and self.tabuleiro[i + 2][j + 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                        # se casas diagonais acima:
                        if(i-1>=0 and i-2>=0):
                            # se a diagonal existe e tem peça oponente:
                            if ((j - 1) >= 0 and (self.tabuleiro[i - 1][j - 1] == 'o' or self.tabuleiro[i - 1][j - 1] == 'O')):
                                # verifica se existe casa vazia na mesma diagonal
                                if ((j - 2) >= 0 and self.tabuleiro[i - 2][j - 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                            # se a outra diagonal existe e tem peça oponente:
                            if ((j + 1) < 8 and (self.tabuleiro[i - 1][j + 1] == 'o' or self.tabuleiro[i - 1][j + 1] == 'O')):
                                # verifica se existe casa vazia na mesma diagonal
                                if ((j + 2) < 8 and self.tabuleiro[i - 2][j + 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                    #se tem dama com jogada obrigatoria
                    elif(self.tabuleiro[i][j] == 'X'):
                        tempi = i
                        tempj = j
                        while(tempi>=0 and tempj>=0):
                            if(tempi-1>=0 and tempj-1>=0 and tempi-2>=0 and tempj-2>=0):
                                if(self.tabuleiro[tempi-1][tempj-1] == 'o' or self.tabuleiro[tempi-1][tempj-1] == 'O'):
                                    if(self.tabuleiro[tempi-2][tempj-2] == '-'):
                                        Obrigatorias.append(self.tabuleirodes[i][j])
                                        break
                                    elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                        break
                            tempi = tempi - 1
                            tempj = tempj - 1
                        tempi = i
                        tempj = j
                        while (tempi >= 0 and tempj < 8):
                            if ((tempi - 1 >= 0) and (tempj + 1 < 8) and (tempi - 2 >= 0) and (tempj + 2 < 8)):
                                if (self.tabuleiro[tempi - 1][tempj + 1] == 'o' or self.tabuleiro[tempi - 1][tempj + 1] == 'O'):
                                    if (self.tabuleiro[tempi - 2][tempj + 2] == '-'):
                                        Obrigatorias.append(self.tabuleirodes[i][j])
                                        break
                                    elif (self.tabuleiro[tempi - 2][tempj + 2] != '-'):
                                        break
                            tempi = tempi - 1
                            tempj = tempj + 1
                        tempi = i
                        tempj = j
                        while (tempi < 8 and tempj >= 0):
                            if ((tempi + 1 < 8) and (tempj - 1 >= 0) and (tempi + 2 < 8) and (tempj - 2 >= 0)):
                                if (self.tabuleiro[tempi + 1][tempj - 1] == 'o' or self.tabuleiro[tempi + 1][tempj - 1] == 'O'):
                                    if (self.tabuleiro[tempi + 2][tempj - 2] == '-'):
                                        Obrigatorias.append(self.tabuleirodes[i][j])
                                        break
                                    elif (self.tabuleiro[tempi + 2][tempj - 2] != '-'):
                                        break
                            tempi = tempi + 1
                            tempj = tempj - 1
                        tempi = i
                        tempj = j
                        while (tempi < 8 and tempj < 8):
                            if ((tempi + 1 < 8) and (tempj + 1 < 8) and (tempi + 2 < 8) and (tempj + 2 < 8)):
                                if (self.tabuleiro[tempi + 1][tempj + 1] == 'o' or self.tabuleiro[tempi + 1][tempj + 1] == 'O'):
                                    if (self.tabuleiro[tempi + 2][tempj + 2] == '-'):
                                        Obrigatorias.append(self.tabuleirodes[i][j])
                                        break
                                    elif (self.tabuleiro[tempi + 2][tempj + 2] != '-'):
                                        break
                            tempi = tempi + 1
                            tempj = tempj + 1
        if(self.turno == 1):
            for i in range (8):
                for j in range (8):
                    if(self.tabuleiro[i][j] == 'o'):
                        if (i + 1 < 8 and i + 2 < 8):
                            # se a casa diagonal existe e tem peça oponente:
                            if ((j - 1) >= 0 and (self.tabuleiro[i + 1][j - 1] == 'x' or self.tabuleiro[i + 1][j - 1] == 'X')):
                                # verifica se existe casa vazia na mesma diagonal
                                if ((j - 2) >= 0 and self.tabuleiro[i + 2][j - 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                            # se a outra diagonal existe e tem peça oponente:
                            if ((j + 1) < 8 and (self.tabuleiro[i + 1][j + 1] == 'x' or self.tabuleiro[i + 1][j + 1] == 'X')):
                                # verifica se existe casa vazia na mesma diagonal
                                if ((j + 2) < 8 and self.tabuleiro[i + 2][j + 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                        if (i - 1 >= 0 and i - 2 >=0):
                            # se a outra casa diagonal existe e tem peça oponente:
                            if ((j - 1) >= 0 and (self.tabuleiro[i - 1][j - 1] == 'x' or self.tabuleiro[i - 1][j - 1] == 'X')):
                                # verifica se existe casa vazia na mesma diagonal
                                if ((j - 2) >= 0 and self.tabuleiro[i - 2][j - 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                            #se a outra diagonal existe e tem peça oponente:
                            if ((j + 1) < 8 and (self.tabuleiro[i - 1][j + 1] == 'x' or self.tabuleiro[i - 1][j + 1] == 'X')):
                                #verifica se existe casa vazia na mesma diagonal
                                if ((j + 2) < 8 and self.tabuleiro[i - 2][j + 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                    #se tem dama com jogada obrigatoria
                    elif (self.tabuleiro[i][j] == 'O'):
                        tempi = i
                        tempj = j
                        while (tempi >= 0 and tempj >= 0):
                            if (tempi - 1 >= 0 and tempj - 1 >= 0 and tempi - 2 >= 0 and tempj - 2 >= 0):
                                if (self.tabuleiro[tempi - 1][tempj - 1] == 'x' or self.tabuleiro[tempi - 1][tempj - 1] == 'X'):
                                    if (self.tabuleiro[tempi - 2][tempj - 2] == '-'):
                                        Obrigatorias.append(self.tabuleirodes[i][j])
                                        break
                                    elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                                        break
                            tempi = tempi - 1
                            tempj = tempj - 1
                        tempi = i
                        tempj = j
                        while (tempi >= 0 and tempj < 8):
                            if ((tempi - 1 >= 0) and (tempj + 1 < 8) and (tempi - 2 >= 0) and (tempj + 2 < 8)):
                                if (self.tabuleiro[tempi - 1][tempj + 1] == 'x' or self.tabuleiro[tempi - 1][tempj + 1] == 'X'):
                                    if (self.tabuleiro[tempi - 2][tempj + 2] == '-'):
                                        Obrigatorias.append(self.tabuleirodes[i][j])
                                        break
                                    elif (self.tabuleiro[tempi - 2][tempj + 2] != '-'):
                                        break
                            tempi = tempi - 1
                            tempj = tempj + 1
                        tempi = i
                        tempj = j
                        while (tempi < 8 and tempj >= 0):
                            if ((tempi + 1 < 8) and (tempj - 1 >= 0) and (tempi + 2 < 8) and (tempj - 2 >= 0)):
                                if (self.tabuleiro[tempi + 1][tempj - 1] == 'x' or self.tabuleiro[tempi + 1][tempj - 1] == 'X'):
                                    if (self.tabuleiro[tempi + 2][tempj - 2] == '-'):
                                        Obrigatorias.append(self.tabuleirodes[i][j])
                                        break
                                    elif (self.tabuleiro[tempi + 2][tempj - 2] != '-'):
                                        break
                            tempi = tempi + 1
                            tempj = tempj - 1
                        tempi = i
                        tempj = j
                        while (tempi < 8 and tempj < 8):
                            if ((tempi + 1 < 8) and (tempj + 1 < 8) and (tempi + 2 < 8) and (tempj + 2 < 8)):
                                if (self.tabuleiro[tempi + 1][tempj + 1] == 'x' or self.tabuleiro[tempi + 1][tempj + 1] == 'X'):
                                    if (self.tabuleiro[tempi + 2][tempj + 2] == '-'):
                                        Obrigatorias.append(self.tabuleirodes[i][j])
                                        break
                                    elif (self.tabuleiro[tempi + 2][tempj + 2] != '-'):
                                        break
                            tempi = tempi + 1
                            tempj = tempj + 1

        if (Obrigatorias != []):
            return Obrigatorias
        return None

    def comer(self, coordpecai, coordpecaj, coordjogi, coordjogj):
        if (coordpecai > coordjogi) and (coordpecaj > coordjogj):
            i = coordpecai - 1
            j = coordpecaj - 1
            while(i > coordjogi) and (j > coordjogj):
                self.tabuleiro[i][j] = '-'
                i = i - 1
                j = j - 1
        elif (coordpecai > coordjogi) and (coordpecaj < coordjogj):
            i = coordpecai - 1
            j = coordpecaj + 1
            while (i > coordjogi) and (j < coordjogj):
                self.tabuleiro[i][j] = '-'
                i = i - 1
                j = j + 1
        elif (coordpecai < coordjogi) and (coordpecaj > coordjogj):
            i = coordpecai + 1
            j = coordpecaj - 1
            while (i < coordjogi) and (j > coordjogj):
                self.tabuleiro[i][j] = '-'
                i = i + 1
                j = j - 1
        elif (coordpecai < coordjogi) and (coordpecaj < coordjogj):
            i = coordpecai + 1
            j = coordpecaj + 1
            while (i < coordjogi) and (j < coordjogj):
                self.tabuleiro[i][j] = '-'
                i = i + 1
                j = j + 1
        return None

    def encadeamento(self, i, j, peca):
        listaencadeamento = []
        #verificar para peao x
        if(peca == 'x'):
            # se casas diagonais abaixo:
            if (i + 1 < 8 and i + 2 < 8):
                # se a diagonal existe e tem peça oponente:
                if ((j - 1) >= 0 and (self.tabuleiro[i + 1][j - 1] == 'o' or self.tabuleiro[i + 1][j - 1] == 'O')):
                    # verifica se existe casa vazia na mesma diagonal
                    if ((j - 2) >= 0 and self.tabuleiro[i + 2][j - 2] == '-'):
                        listaencadeamento.append(self.tabuleirodes[i][j])
                # se a outra diagonal existe e tem peça oponente:
                if ((j + 1) < 8 and (self.tabuleiro[i + 1][j + 1] == 'o' or self.tabuleiro[i + 1][j + 1] == 'O')):
                    # verifica se existe casa vazia na mesma diagonal
                    if ((j + 2) < 8 and self.tabuleiro[i + 2][j + 2] == '-'):
                        listaencadeamento.append(self.tabuleirodes[i][j])
            # se casas diagonais acima:
            if (i - 1 >= 0 and i - 2 >= 0):
                # se a diagonal existe e tem peça oponente:
                if ((j - 1) >= 0 and (self.tabuleiro[i - 1][j - 1] == 'o' or self.tabuleiro[i - 1][j - 1] == 'O')):
                    # verifica se existe casa vazia na mesma diagonal
                    if ((j - 2) >= 0 and self.tabuleiro[i - 2][j - 2] == '-'):
                        listaencadeamento.append(self.tabuleirodes[i][j])
                # se a outra diagonal existe e tem peça oponente:
                if ((j + 1) < 8 and (self.tabuleiro[i - 1][j + 1] == 'o' or self.tabuleiro[i - 1][j + 1] == 'O')):
                    # verifica se existe casa vazia na mesma diagonal
                    if ((j + 2) < 8 and self.tabuleiro[i - 2][j + 2] == '-'):
                        listaencadeamento.append(self.tabuleirodes[i][j])
        # Verificar encadeamento de dama X
        elif (self.tabuleiro[i][j] == 'X'):
            tempi = i
            tempj = j
            while (tempi >= 0 and tempj >= 0):
                if (tempi - 1 >= 0 and tempj - 1 >= 0 and tempi - 2 >= 0 and tempj - 2 >= 0):
                    if (self.tabuleiro[tempi - 1][tempj - 1] == 'o' or self.tabuleiro[tempi - 1][tempj - 1] == 'O'):
                        if (self.tabuleiro[tempi - 2][tempj - 2] == '-'):
                            listaencadeamento.append(self.tabuleirodes[i][j])
                            break
                        elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                            break
                tempi = tempi - 1
                tempj = tempj - 1
            tempi = i
            tempj = j
            while (tempi >= 0 and tempj < 8):
                if ((tempi - 1 >= 0) and (tempj + 1 < 8) and (tempi - 2 >= 0) and (tempj + 2 < 8)):
                    if (self.tabuleiro[tempi - 1][tempj + 1] == 'o' or self.tabuleiro[tempi - 1][tempj + 1] == 'O'):
                        if (self.tabuleiro[tempi - 2][tempj + 2] == '-'):
                            listaencadeamento.append(self.tabuleirodes[i][j])
                            break
                        elif (self.tabuleiro[tempi - 2][tempj + 2] != '-'):
                            break
                tempi = tempi - 1
                tempj = tempj + 1
            tempi = i
            tempj = j
            while (tempi < 8 and tempj >= 0):
                if ((tempi + 1 < 8) and (tempj - 1 >= 0) and (tempi + 2 < 8) and (tempj - 2 >= 0)):
                    if (self.tabuleiro[tempi + 1][tempj - 1] == 'o' or self.tabuleiro[tempi + 1][tempj - 1] == 'O'):
                        if (self.tabuleiro[tempi + 2][tempj - 2] == '-'):
                            listaencadeamento.append(self.tabuleirodes[i][j])
                            break
                        elif (self.tabuleiro[tempi + 2][tempj - 2] != '-'):
                            break
                tempi = tempi + 1
                tempj = tempj - 1
            tempi = i
            tempj = j
            while (tempi < 8 and tempj < 8):
                if ((tempi + 1 < 8) and (tempj + 1 < 8) and (tempi + 2 < 8) and (tempj + 2 < 8)):
                    if (self.tabuleiro[tempi + 1][tempj + 1] == 'o' or self.tabuleiro[tempi + 1][tempj + 1] == 'O'):
                        if (self.tabuleiro[tempi + 2][tempj + 2] == '-'):
                            listaencadeamento.append(self.tabuleirodes[i][j])
                            break
                        elif (self.tabuleiro[tempi + 2][tempj + 2] != '-'):
                            break
                tempi = tempi + 1
                tempj = tempj + 1
        #encadeamento de peao o
        if (peca == 'o'):
            if (i + 1 < 8 and i + 2 < 8):
                # se a casa diagonal existe e tem peça oponente:
                if ((j - 1) >= 0 and (self.tabuleiro[i + 1][j - 1] == 'x' or self.tabuleiro[i + 1][j - 1] == 'X')):
                    # verifica se existe casa vazia na mesma diagonal
                    if ((j - 2) >= 0 and self.tabuleiro[i + 2][j - 2] == '-'):
                        listaencadeamento.append(self.tabuleirodes[i][j])
                # se a outra diagonal existe e tem peça oponente:
                if ((j + 1) < 8 and (self.tabuleiro[i + 1][j + 1] == 'x' or self.tabuleiro[i + 1][j + 1] == 'X')):
                    # verifica se existe casa vazia na mesma diagonal
                    if ((j + 2) < 8 and self.tabuleiro[i + 2][j + 2] == '-'):
                        listaencadeamento.append(self.tabuleirodes[i][j])
            if (i - 1 >= 0 and i - 2 >= 0):
                # se a outra casa diagonal existe e tem peça oponente:
                if ((j - 1) >= 0 and (self.tabuleiro[i - 1][j - 1] == 'x' or self.tabuleiro[i - 1][j - 1] == 'X')):
                    # verifica se existe casa vazia na mesma diagonal
                    if ((j - 2) >= 0 and self.tabuleiro[i - 2][j - 2] == '-'):
                        listaencadeamento.append(self.tabuleirodes[i][j])
                # se a outra diagonal existe e tem peça oponente:
                if ((j + 1) < 8 and (self.tabuleiro[i - 1][j + 1] == 'x' or self.tabuleiro[i - 1][j + 1] == 'X')):
                    # verifica se existe casa vazia na mesma diagonal
                    if ((j + 2) < 8 and self.tabuleiro[i - 2][j + 2] == '-'):
                        listaencadeamento.append(self.tabuleirodes[i][j])
        # Encadeamento de dama O
        elif (peca == 'O'):
            tempi = i
            tempj = j
            while (tempi >= 0 and tempj >= 0):
                if (tempi - 1 >= 0 and tempj - 1 >= 0 and tempi - 2 >= 0 and tempj - 2 >= 0):
                    if (self.tabuleiro[tempi - 1][tempj - 1] == 'x' or self.tabuleiro[tempi - 1][tempj - 1] == 'X'):
                        if (self.tabuleiro[tempi - 2][tempj - 2] == '-'):
                            listaencadeamento.append(self.tabuleirodes[i][j])
                            break
                        elif (self.tabuleiro[tempi - 2][tempj - 2] != '-'):
                            break
                tempi = tempi - 1
                tempj = tempj - 1
            tempi = i
            tempj = j
            while (tempi >= 0 and tempj < 8):
                if ((tempi - 1 >= 0) and (tempj + 1 < 8) and (tempi - 2 >= 0) and (tempj + 2 < 8)):
                    if (self.tabuleiro[tempi - 1][tempj + 1] == 'x' or self.tabuleiro[tempi - 1][tempj + 1] == 'X'):
                        if (self.tabuleiro[tempi - 2][tempj + 2] == '-'):
                            listaencadeamento.append(self.tabuleirodes[i][j])
                            break
                        elif (self.tabuleiro[tempi - 2][tempj + 2] != '-'):
                            break
                tempi = tempi - 1
                tempj = tempj + 1
            tempi = i
            tempj = j
            while (tempi < 8 and tempj >= 0):
                if ((tempi + 1 < 8) and (tempj - 1 >= 0) and (tempi + 2 < 8) and (tempj - 2 >= 0)):
                    if (self.tabuleiro[tempi + 1][tempj - 1] == 'x' or self.tabuleiro[tempi + 1][tempj - 1] == 'X'):
                        if (self.tabuleiro[tempi + 2][tempj - 2] == '-'):
                            listaencadeamento.append(self.tabuleirodes[i][j])
                            break
                        elif (self.tabuleiro[tempi + 2][tempj - 2] != '-'):
                            break
                tempi = tempi + 1
                tempj = tempj - 1
            tempi = i
            tempj = j
            while (tempi < 8 and tempj < 8):
                if ((tempi + 1 < 8) and (tempj + 1 < 8) and (tempi + 2 < 8) and (tempj + 2 < 8)):
                    if (self.tabuleiro[tempi + 1][tempj + 1] == 'x' or self.tabuleiro[tempi + 1][tempj + 1] == 'X'):
                        if (self.tabuleiro[tempi + 2][tempj + 2] == '-'):
                            listaencadeamento.append(self.tabuleirodes[i][j])
                            break
                        elif (self.tabuleiro[tempi + 2][tempj + 2] != '-'):
                            break
                tempi = tempi + 1
                tempj = tempj + 1
        if(listaencadeamento != []):
            return listaencadeamento
        return None

    def turnojogador(self):
        #verificar se há jogadas obrigatorias
        if(self.continuapulo == 0):
            self.lista_obrigatorias = self.verificarObrigatorias()
        #se não há jogadas obrigatorias verificar se há jogadas validas
        if(self.lista_obrigatorias == None):
            valido = self.verificarsehajogadaspossiveis('o', 'O')
            # print("valido: ", valido)
            if(valido == 0):
                self.cena.setCena("lose")
        #print(self.lista_obrigatorias)
        self.lista_possibilidades = self.verificarjogadas()
        # print("obrigatorias: ", self.lista_obrigatorias)
        # print("Possibilidades: ", self.lista_possibilidades)
        #definir peça
        peca = ''
        # Se houver, Recuperar casa selecionada na matriz de jogo
        if(self.casa_selecionada):
            for i in range(8):
                for j in range(8):
                    if (self.tabuleirodes[i][j].x == self.selecionada.x) and (
                            self.tabuleirodes[i][j].y == self.selecionada.y):
                        peca = (i, j)
        #verificar se ha clique no mouse
        if(self.mouse.is_button_pressed(1)):
            #print("entrou no loop")
            #verifica se há célula selecionada
            if(self.casa_selecionada):
                #print("achou casa selecionada")
                #se a peça na casa selecionada pertence ao jogador
                if (peca) and (self.tabuleiro[peca[0]][peca[1]] == 'o' or self.tabuleiro[peca[0]][peca[1]] == 'O'):
                    #print("a peça da seleção tem a peça do jogador")
                    #verifica se há jogadas possiveis
                    if(self.lista_possibilidades):
                        #onde foi o clique:
                        jogadai = ''
                        jogadaj = ''
                        pos = self.mouse.get_position()
                        for i in range(8):
                            for j in range(8):
                                if ((self.tabuleirodes[i][j].x < pos[0]) and ((self.tabuleirodes[i][j].x + self.tamcasa) > pos[0]) and (self.tabuleirodes[i][j].y < pos[1]) and ((self.tabuleirodes[i][j].y + self.tamcasa) > pos[1])):
                                    jogadai = i
                                    jogadaj = j
                        #verifica se o clique foi em celula possivel
                        for elemento in self.lista_possibilidades:
                            #print("chegou aqui ", "peca ",peca[0], peca[1], "jogada ", jogadai, jogadaj)
                            #print("compara x:", elemento.x, self.tabuleirodes[jogadai][jogadaj].x)
                            #print("compara y:", elemento.y, self.tabuleirodes[jogadai][jogadaj].y)
                            if ((elemento.x == self.tabuleirodes[jogadai][jogadaj].x)and(elemento.y == self.tabuleirodes[jogadai][jogadaj].y)):
                                #jogada valida, prosseguir troca
                                #print("valida-prosseguir troca")
                                temp = self.tabuleiro[jogadai][jogadaj]
                                self.tabuleiro[jogadai][jogadaj] = self.tabuleiro[peca[0]][peca[1]]
                                self.tabuleiro[peca[0]][peca[1]] = temp
                                if self.pulo == 1:
                                    self.continuapulo = 0
                                    self.comer(peca[0], peca[1], jogadai, jogadaj)
                                    self.pulo = 0
                                    #print(self.tabuleiro[jogadai][jogadaj])
                                    self.lista_obrigatorias = self.encadeamento(jogadai, jogadaj, self.tabuleiro[jogadai][jogadaj])
                                    #print(self.lista_obrigatorias)
                                    if(self.lista_obrigatorias != None):
                                        self.continuapulo = 1
                                        self.pulo = 1
                                        #print("continua pulo")
                                    else:
                                        self.turno = 0
                                        #print("virou turno")
                                else:
                                    self.turno = 0
                                    #print("virou turno")
                                #print("jogou")
                                self.casa_selecionada = None
                                self.lista_possibilidades = None
                            else:
                                self.selecionar()
                    #se não há, selecionar
                    self.selecionar()
                else:
                    self.selecionar()
            else:
                self.selecionar()
        return None

    def turnoia(self):
        #forçar reinicio da casa selecionada caso esteja presa em uma peça oponente:
        if(self.casa_selecionada):
            coorselecionada = None
            for i in range(8):
                for j in range(8):
                    if (self.tabuleirodes[i][j].x == self.casa_selecionada.x) and (self.tabuleirodes[i][j].y == self.casa_selecionada.y):
                        coorselecionada = (i, j)
            if(self.tabuleiro[coorselecionada[0]][coorselecionada[1]]=='x' or self.tabuleiro[coorselecionada[0]][coorselecionada[1]]=='X'):
                print("selecao correta para o turno")
            else:
                self.casa_selecionada = None
        if(self.casa_selecionada == None):
            pecaselecionada = None
            # verificar se há jogadas obrigatorias e montar lista
            if (self.continuapulo == 0):
                self.lista_obrigatorias = self.verificarObrigatorias()
            # se não há jogadas obrigatorias verificar se há jogadas validas se houver listar peças com essas jogadas
            if (self.lista_obrigatorias == None):
                possibilidades = self.jogadaspossiveisIA()
                #se não há jogadas obrigatórias nem jogadas possiveis, IA perde, jogador vence
                if (possibilidades == None):
                    self.cena.setCena("win")
            #se tem obrigatorias ela se torna lista da seleção
            if(self.lista_obrigatorias != None):
                pecaselecionada = random.choice(self.lista_obrigatorias)
            elif(possibilidades != None):
                pecaselecionada = random.choice(possibilidades)
            #seleciona a peça
            if(pecaselecionada):
                self.casa_selecionada = pecaselecionada
        else:
            #verifica possibilidades de jogo
            self.lista_possibilidades = self.verificarjogadas()
            # definir peça
            peca = ''
            # Se houver, Recuperar posição da casa selecionada na matriz de jogo
            if (self.casa_selecionada):
                for i in range(8):
                    for j in range(8):
                        if (self.tabuleirodes[i][j].x == self.casa_selecionada.x) and (self.tabuleirodes[i][j].y == self.casa_selecionada.y):
                            peca = (i, j)
            #escolher na lista de jogadas possiveis uma para movimentar
            jogada = random.choice(self.lista_possibilidades)
            #recuperar as coordenadas pra casa escolhida para a jogada
            coordjogada = ''
            if (jogada):
                for i in range(8):
                    for j in range(8):
                        if (self.tabuleirodes[i][j].x == jogada.x) and (self.tabuleirodes[i][j].y == jogada.y):
                            coordjogada = (i, j)
            #prosseguir a jogada
            if(peca and coordjogada):
                #procedimento de atualização da matriz
                temp = self.tabuleiro[coordjogada[0]][coordjogada[1]]
                self.tabuleiro[coordjogada[0]][coordjogada[1]] = self.tabuleiro[peca[0]][peca[1]]
                self.tabuleiro[peca[0]][peca[1]] = temp
                #se pulo foi detectado
                if self.pulo == 1:
                    self.continuapulo = 0
                    self.comer(peca[0], peca[1], coordjogada[0], coordjogada[1])
                    self.pulo = 0
                    print(self.tabuleiro[coordjogada[0]][coordjogada[1]])
                    #verificar encadeamento
                    self.lista_obrigatorias = self.encadeamento(coordjogada[0], coordjogada[1],self.tabuleiro[coordjogada[0]][coordjogada[1]])
                    print(self.lista_obrigatorias)
                    #se a lista de obrigatorias (resultado de encadeamente ficou diferente de vazia, o pulo continua
                    if (self.lista_obrigatorias != None):
                        self.continuapulo = 1
                        self.pulo = 1
                        print("continua pulo")
                    #senão o turno vira
                    else:
                        self.turno = 1
                        print("virou turno")
                #se não há pulo, o turno vira
                else:
                    self.turno = 1
                    print("virou turno")
                #fim da jogada da IA
                print("jogou")
                self.casa_selecionada = None
                self.lista_possibilidades = None
                self.atraso = 1
        return None

    def jogadaspossiveisIA(self):
        possibilidades = []
        # pra cada celula
        for i in range(8):
            for j in range(8):
                #para peões
                if (self.tabuleiro[i][j] == 'x'):
                    # verifica casas diagonais abaixo - A IA joga para baixo se movimento for possivel, acrescentar essa celula a lista
                    if ((j - 1) >= 0 and self.tabuleiro[i + 1][j - 1] == '-'):
                        possibilidades.append(self.tabuleirodes[i][j])
                    if ((j + 1) < 8 and self.tabuleiro[i + 1][j + 1] == '-'):
                        possibilidades.append(self.tabuleirodes[i][j])
                #para damas
                elif (self.tabuleiro[i][j] == 'X'):
                    controle = 0 #variavel de controle, uma vez que uma peça foi add a lista, não será novamente
                    tempi = i - 1
                    tempj = j - 1
                    while (tempi >= 0 and tempj >= 0):
                        if (self.tabuleiro[tempi][tempj] == '-'):
                            possibilidades.append(self.tabuleirodes[i][j])
                            controle = 1
                            break
                        else:
                            break
                        tempi = tempi - 1
                        tempj = tempj - 1
                    if (controle == 0):
                        tempi = i - 1
                        tempj = j + 1
                        while (tempi >= 0 and tempj < 8):
                            if (self.tabuleiro[tempi][tempj] == '-'):
                                possibilidades.append(self.tabuleirodes[i][j])
                                controle = 1
                                break
                            else:
                                break
                            tempi = tempi - 1
                            tempj = tempj + 1
                    if (controle == 0):
                        tempi = i + 1
                        tempj = j - 1
                        while (tempi < 8 and tempj >= 0):
                            if (self.tabuleiro[tempi][tempj] == '-'):
                                possibilidades.append(self.tabuleirodes[i][j])
                                controle = 1
                                break
                            else:
                                break
                            tempi = tempi + 1
                            tempj = tempj - 1
                    if (controle == 0):
                        tempi = i + 1
                        tempj = j + 1
                        while (tempi < 8 and tempj < 8):
                            if (self.tabuleiro[tempi][tempj] == '-'):
                                possibilidades.append(self.tabuleirodes[i][j])
                                controle = 1
                            else:
                                break
                            tempi = tempi + 1
                            tempj = tempj + 1
        # a lista de casas possiveis
        if(possibilidades!= []):
            return possibilidades
        return None
    def verificavitoria(self):
        temX = 0
        temO = 0
        for i in range (8):
            for j in range (8):
                if (self.tabuleiro[i][j] == 'x') or (self.tabuleiro[i][j] == 'X'):
                    temX = 1
                    break
        for i in range (8):
            for j in range (8):
                if(self.tabuleiro[i][j] == 'o') or (self.tabuleiro[i][j] == 'O'):
                    temO = 1
                    break
        if(temX == 0):
            self.cena.setCena("win")
        elif(temO == 0):
            self.cena.setCena("lose")
        return None

    def jogo(self):
        #se ha atraso
        if(self.atraso == 1):
            self.window.delay(1000)
            self.atraso = 0
        #desenhar tabuleiro
        self.bggame.draw()
        self.desenhatabuleiro()
        self.desenhajogo()
        if (self.turno == 1):
            self.turnojogador()
        else:
            self.turnoia()
        self.verificaDama()
        self.verificavitoria()