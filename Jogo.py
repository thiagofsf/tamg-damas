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
        self.xini = 186
        self.yini = 0
        self.tamcasa = 60

        self.turno = 1
        self.jogadores = ('x', 'o')
        self.casa_selecionada = None
        self.lista_possibilidades = None
        self.lista_obrigatorias = None
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
        self.tabuleiro2 = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                          ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
                          ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', '-', '-', '-', '-', '-', '-', '-'],
                          ['-', 'o', '-', 'o', '-', 'o', '-', 'o'],
                          ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
                          ['-', 'o', '-', 'o', '-', 'o', '-', 'o']]

        self.tabuleiro = [['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                          ['-', 'x', '-', 'x', '-', 'x', '-', 'x'],
                          ['x', '-', 'x', '-', 'x', '-', 'x', '-'],
                          ['-', '-', '-', '-', '-', 'o', '-', '-'],
                          ['-', '-', '-', '-', 'x', '-', '-', '-'],
                          ['-', 'o', '-', '-', '-', 'o', '-', 'o'],
                          ['o', '-', 'o', '-', 'o', '-', 'o', '-'],
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
        pygame.time.wait(200)
        return None

    def verificarjogadas(self):
        #lista de marcadas
        if(self.casa_selecionada):
            possibilidades = []
            if(self.lista_obrigatorias):
                print("verificando jogadas -> tem obrigatoria")
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
                                            possibilidades.append(self.tabuleirodes[i][j])
                                            self.pulo = 1
                                #verificar casas diagonais acima
                                if(i-1 >=0 and i-2>=0):
                                    # se a casa diagonal existe e tem peça oponente:
                                    if ((j - 1) >= 0 and (self.tabuleiro[i - 1][j - 1] == 'o' or self.tabuleiro[i - 1][j - 1] == 'O')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j - 2) >= 0 and self.tabuleiro[i - 2][j - 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i - 2][j - 2])
                                            self.pulo = 1
                                    # se a outra diagonal existe e tem peça oponente:
                                    if ((j + 1) < 8 and (self.tabuleiro[i - 1][j + 1] == 'o' or self.tabuleiro[i - 1][j + 1] == 'O')):
                                        # verifica se existe casa vazia na mesma diagonal
                                        if ((j + 2) < 8 and self.tabuleiro[i - 2][j + 2] == '-'):
                                            possibilidades.append(self.tabuleirodes[i - 2][j + 2])
                                            self.pulo = 1
                            if(self.tabuleiro[i][j] == 'o'):
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
                                            possibilidades.append(self.tabuleirodes[i][j])
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
                            elif(self.tabuleiro[i][j] == self.jogadores[1]):
                                # verifica casas diagonais acima
                                if ((j-1)>=0 and self.tabuleiro[i - 1][j - 1] == '-'):
                                    possibilidades.append(self.tabuleirodes[i - 1][j - 1])
                                if ((j+1)<8 and self.tabuleiro[i - 1][j + 1] == '-'):
                                    possibilidades.append(self.tabuleirodes[i - 1][j + 1])
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
        if(self.turno == 1):
            for i in range (8):
                for j in range (8):
                    if(self.tabuleiro[i][j] == 'o'):
                        if (i + 1 < 8 and i + 2 < 8):
                            # se a casa diagonal existe e tem peça oponente:
                            if ((j - 1) >= 0 and (
                                    self.tabuleiro[i + 1][j - 1] == 'x' or self.tabuleiro[i + 1][j - 1] == 'X')):
                                # verifica se existe casa vazia na mesma diagonal
                                if ((j - 2) >= 0 and self.tabuleiro[i + 2][j - 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                            # se a outra diagonal existe e tem peça oponente:
                            if ((j + 1) < 8 and (
                                    self.tabuleiro[i + 1][j + 1] == 'x' or self.tabuleiro[i + 1][j + 1] == 'X')):
                                # verifica se existe casa vazia na mesma diagonal
                                if ((j + 2) < 8 and self.tabuleiro[i + 2][j + 2] == '-'):
                                    Obrigatorias.append(self.tabuleirodes[i][j])
                        if (i < 1 >= 8 and i - 2 >=0):
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
        if (Obrigatorias != []):
            return Obrigatorias
        return None

    def turnojogador(self):
        #verificar se há jogadas obrigatorias
        self.lista_obrigatorias = self.verificarObrigatorias()
        self.lista_possibilidades = self.verificarjogadas()
        #print("obrigatorias: ", self.lista_obrigatorias)
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
            print("entrou no loop")
            #verifica se há célula selecionada
            if(self.casa_selecionada):
                print("achou casa selecionada")
                #se a peça na casa selecionada pertence ao jogador
                if (peca) and (self.tabuleiro[peca[0]][peca[1]] == 'o'):
                    print("a peça da seleção tem a peça do jogador")
                    #verifica se há jogadas possiveis
                    if(self.lista_possibilidades):
                        #onde foi o clique:
                        jogadai = ''
                        jogadaj = ''
                        pos = self.mouse.get_position()
                        for i in range(8):
                            for j in range(8):
                                if ((self.tabuleirodes[i][j].x < pos[0]) and (
                                        (self.tabuleirodes[i][j].x + self.tamcasa) > pos[0]) and (
                                        self.tabuleirodes[i][j].y < pos[1]) and (
                                        (self.tabuleirodes[i][j].y + self.tamcasa) > pos[1])):
                                    jogadai = i
                                    jogadaj = j
                        #verifica se o clique foi em celula possivel
                        for elemento in self.lista_possibilidades:
                            print("chegou aqui ", "peca ",peca[0], peca[1], "jogada ", jogadai, jogadaj)
                            print("compara x:", elemento.x, self.tabuleirodes[jogadai][jogadaj].x)
                            print("compara y:", elemento.y, self.tabuleirodes[jogadai][jogadaj].y)
                            if ((elemento.x == self.tabuleirodes[jogadai][jogadaj].x)and(elemento.y == self.tabuleirodes[jogadai][jogadaj].y)):
                                #jogada valida, prosseguir troca
                                print("valida-prosseguir troca")
                                temp = self.tabuleiro[jogadai][jogadaj]
                                self.tabuleiro[jogadai][jogadaj] = self.tabuleiro[peca[0]][peca[1]]
                                self.tabuleiro[peca[0]][peca[1]] = temp
                                if self.pulo == 1:
                                    self.comer(peca[0], peca[1], jogadai, jogadaj)
                                    self.pulo = 0
                                print("jogou")
                                #self.turno = 0
                                self.casa_selecionada = None
                                self.lista_possibilidades = None
                                self.lista_obrigatorias = None
                            else:
                                self.selecionar()
                    #se não há, selecionar
                    self.selecionar()
                else:
                    self.selecionar()
            else:
                self.selecionar()

        return None
    def comer(self, coordpecai, coordpecaj, coordjogi, coordjogj):
        if (coordpecai > coordjogi) and (coordpecaj > coordjogj):
            self.tabuleiro[coordpecai-1][coordpecaj-1] = '-'
        elif (coordpecai > coordjogi) and (coordpecaj < coordjogj):
            self.tabuleiro[coordpecai - 1][coordpecaj + 1] = '-'
        elif (coordpecai < coordjogi) and (coordpecaj > coordjogj):
            self.tabuleiro[coordpecai + 1][coordpecaj - 1] = '-'
        elif (coordpecai < coordjogi) and (coordpecaj < coordjogj):
            self.tabuleiro[coordpecai + 1][coordpecaj + 1] = '-'
        return None

    def turnoia(self):
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
            self.cena = "win"
        elif(temO == 0):
            self.cena = "lose"
        return None

    def jogo(self):
        #desenhar tabuleiro
        self.bggame.draw()
        self.desenhatabuleiro()
        self.desenhajogo()
        if (self.turno == 1):
            self.turnojogador()
        else:
            self.turnoia()
        self.verificavitoria()


