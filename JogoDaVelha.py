# -*- coding: utf-8 -*-
import random

class quadrado:
    def __init__(self):
        self.vencedor = "-"
    
    def marca(self, jogador):
        self.vencedor = jogador

class Tabuleiro:
    def __init__(self):
        self.espacos_X = 0
        self.espacos_O = 0
        self.posicoesLivres = [0,1,2,3,4,5,6,7,8]
        self.vencedor = None

    def verificaVencedor(self, jogador, linha, coluna, tabuleiro):
        if tabuleiro[linha][0].vencedor == tabuleiro[linha][1].vencedor == tabuleiro[linha][2].vencedor:
            return True

        elif tabuleiro[0][coluna].vencedor == tabuleiro[1][coluna].vencedor == tabuleiro[2][coluna].vencedor:
            return True
        
        elif linha == coluna or (linha==0 and coluna==2) or (linha==2 and coluna ==0):
            if tabuleiro[0][0].vencedor == tabuleiro[1][1].vencedor == tabuleiro[2][2].vencedor == jogador:
                return True
            elif tabuleiro[0][2].vencedor == tabuleiro[1][1].vencedor == tabuleiro[2][0].vencedor == jogador:
                return True
    
    def checaMarcacao(self, linha, coluna, tabuleiro):
        vencedor = tabuleiro[linha][coluna].vencedor
        if vencedor == None or vencedor=="-":
            return False
        return True

class TabuleiroMicro(Tabuleiro):
    def __init__(self):
        Tabuleiro.__init__(self)
        self.tabuleiro = [[quadrado() for i in range(3)] for j in range(3)]

    def imprime(self):
        print(" ───────")
        for i in range(3):
            print("| ", end="")
            for j in range(3):
                print(self.tabuleiro[i][j].vencedor, end=" ")
            print("|")
        print(" ───────")

    def imprimeLinha(self, linha):
        print("| ", end="")
        for j in range(3):
            print(self.tabuleiro[linha][j].vencedor, end=" ")
        print("| ", end="")

    def marcaQuadrado(self, linha, coluna, jogador):
        self.tabuleiro[linha][coluna].marca(jogador)
        self.posicoesLivres.remove(linha*3 + coluna)
        if jogador == "X": 
            self.espacos_X +=1
        else:
            self.espacos_O +=1
        
        vencedor = self.verificaVencedor(jogador, linha, coluna, self.tabuleiro)
        if vencedor:
            self.fechaTabuleiro(jogador)

        elif len(self.posicoesLivres) == 0:
            self.vencedor = "V" #Velha
    
    def fechaTabuleiro(self, jogador):
        self.vencedor = jogador
        self.posicoesLivres.clear()
        print("Micro-tabuleiro fechado: ")
        self.imprime()
        print()
        for i in range(3):
            for j in range(3):
                self.tabuleiro[i][j].vencedor = self.vencedor


class TabuleiroMacro(Tabuleiro):
    def __init__(self):
        Tabuleiro.__init__(self)
        self.tabuleiro = [[TabuleiroMicro() for i in range(3)] for j in range(3)]
        self.fimDeJogo = False

    def imprime(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.tabuleiro[i][k].imprimeLinha(j)
                print()
            print()

    def imprimeMicroTabuleirosDisponiveis(self):
        print("Micro-tabuleiros disponíveis:", end=" ")
        for i in range(len(self.posicoesLivres)):
            print(self.posicoesLivres[i], end=" ")
        print()

    def jogada(self, microTabuleiro, jogador, linha, coluna):
        microTab = self.tabuleiro[microTabuleiro//3][microTabuleiro%3]
        microTab.marcaQuadrado(linha, coluna, jogador)
        if microTab.vencedor == jogador:
            self.posicoesLivres.remove(microTabuleiro)
            if self.verificaVencedor(jogador,microTabuleiro//3, microTabuleiro%3, self.tabuleiro):
                self.posicoesLivres.clear()
                self.vencedor = jogador
                self.fimDeJogo = True
                return
            elif len(self.posicoesLivres) == 0:
                self.vencedor = "V"
                self.fimDeJogo = True


class Jogador:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo
        self.numJogadas = 0
    
class JogadorHumano(Jogador):
    def __init__(self, nome, tipo):
        Jogador.__init__(self, nome, tipo)
    
    def escolhePosicao(self,tabuleiro):
        tabuleiro.imprimeMicroTabuleirosDisponiveis()
        microTabuleiro = int(input("Selecione o micro-tabuleiro que você quer jogar: "))
        
        while tabuleiro.checaMarcacao(microTabuleiro//3,microTabuleiro%3,tabuleiro.tabuleiro):
            print("Esse tabuleiro já está marcado, selecione outro!")
            microTabuleiro = int(input("Selecione o micro-tabuleiro que você quer jogar: "))

        microTab = tabuleiro.tabuleiro[microTabuleiro//3][microTabuleiro%3]
        microTab.imprime()
        posicao = int(input("Selecione a posição que deseja marcar: "))

        while microTab.checaMarcacao(posicao//3,posicao%3,microTab.tabuleiro):
            print("Essa posição já está marcado, selecione outra!")
            posicao = int(input("Selecione a posição que deseja marcar: "))
            
        tabuleiro.jogada(microTabuleiro, self.tipo, posicao//3, posicao%3)
        self.numJogadas += 1

class JogadorComeCru(Jogador):
    def __init__(self,nome,tipo):
        Jogador.__init__(self, nome, tipo)

    def escolhePosicao(self, tabuleiro):
        microTabuleiro = tabuleiro.posicoesLivres[0]
        microTab = tabuleiro.tabuleiro[microTabuleiro//3][microTabuleiro%3]
        linha = microTab.posicoesLivres[0]//3
        coluna = microTab.posicoesLivres[0]%3
        tabuleiro.jogada(microTabuleiro, self.tipo, linha, coluna)
        self.numJogadas+=1

class JogadorEstabanado(Jogador):
    def __init__(self, nome, tipo):
        Jogador.__init__(self, nome, tipo)

    def escolhePosicao(self, tabuleiro):
        indice = random.randint(0,len(tabuleiro.posicoesLivres)-1)
        microTabuleiro = tabuleiro.posicoesLivres[indice]
        microTab = tabuleiro.tabuleiro[microTabuleiro//3][microTabuleiro%3]
        indice = random.randint(0,len(microTab.posicoesLivres)-1)
        linha = microTab.posicoesLivres[indice]//3
        coluna = microTab.posicoesLivres[indice]%3
        tabuleiro.jogada(microTabuleiro,self.tipo,linha, coluna)
        self.numJogadas+=1

def selecionaTipo(tipoJogador, XouO):
    nome = input("Digite o nome desse jogador: ")

    if tipoJogador == 1:
        return JogadorHumano(nome,XouO)
    elif tipoJogador == 2:
        return JogadorEstabanado(nome,XouO)
    elif tipoJogador == 3:
        return JogadorComeCru(nome, XouO)
    else:
        print("\nSelecione um tipo válido")
        print("Tipos de jogadores: \n(1) Humano\n(2) Estabanado\n(3) Come-crú")
        tipoJogador = int(input("Selecione o tipo do Jogador: "))
        jogador = selecionaTipo(tipoJogador, XouO)
        return jogador

def main():
    tabuleiro = TabuleiroMacro()

    print("Tipos de jogadores: \n(1) Humano\n(2) Estabanado\n(3) Come-crú")
    tipoJogador = int(input("Selecione o tipo do Jogador 1: "))
    jogador1 = selecionaTipo(tipoJogador, "X")
    tipoJogador = int(input("Selecione o tipo do Jogador 2: "))
    jogador2 = selecionaTipo(tipoJogador,"O")

    while not(tabuleiro.fimDeJogo):
        tabuleiro.imprime()
        print("\n")
        if jogador1.numJogadas > jogador2.numJogadas:
            print(f'Vez de {jogador2.nome}:')
            jogador2.escolhePosicao(tabuleiro)

        else:
            print(f'Vez de {jogador1.nome}:')
            jogador1.escolhePosicao(tabuleiro)
    tabuleiro.imprime()
    if tabuleiro.vencedor == "V":
        print("O jogo deu velha")
    elif tabuleiro.vencedor == "X":
        print(f'{jogador1.nome} é o vencedor')
    else:
        print(f'{jogador2.nome} é o vencedor')  

if __name__== '__main__':
    main()