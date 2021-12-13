class quadrado:
    def __init__(self, jogador):
        self.vencedor = None
    
    def marca(self, jogador):
        self.vencedor = jogador

class Tabuleiro:
    def __init__(self):
        self.espacos_livre = 9
        self.espacos_X = 0
        self.espacos_O = 0

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
    

class TabuleiroMicro(Tabuleiro):
    def __init__(self):
        Tabuleiro.__init__(self)
        self.tabuleiro = [[quadrado() for i in range(3)] for j in range(3)]
        self.vencedor = None

    def imprime(self):
        print(" ───────")
        for i in range(3):
            print("| ", end="")
            for j in range(3):
                print(self.tabuleiro[2-i][j], end=" ")
            print("|")
        print(" ───────")

    def imprimeLinha(self, linha):
        print("| ", end="")
        for j in range(3):
            print(self.tabuleiro[linha][j], end=" ")
        print("| ", end="")

    def marcaQuadrado(self, linha, coluna, jogador):
        self.tabuleiro[linha][coluna].marca(jogador)
        self.espacos_livre -= 1
        if jogador == "X": 
            self.espacos_X +=1
        else:
            self.espacos_O +=1
        
        vencedor = self.verificaVencedor(jogador, linha, coluna, self.tabuleiro)
        if vencedor:
            self.vencedor = jogador
            for i in range(3):
                for j in range(3):
                    self.tabuleiro[i][j] = self.vencedor


        elif self.espacos_O == self.espacos_X:
            vencedor = "V" #Velha
    
    def checaMarcacao(self, linha, coluna):
        if self.tabuleiro[linha][coluna].vencedor == None:
            return False
        return True

class TabuleiroMacro(Tabuleiro):
    def __init__(self):
        Tabuleiro.__init__(self)
        self.tabuleiro = [[TabuleiroMicro() for i in range(3)] for j in range(3)]

    def imprime(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.tabuleiro[i][k].imprimeLinha(j)
                print()
            print()

    def jogada(self, microTabuleiro, jogador, linha, coluna):
        microTab = self.tabuleiro[microTabuleiro//3][microTabuleiro%3]
        microTab.marcaQuadrado(linha, coluna, jogador)
        if microTab.vencedor == jogador:
            self.espacos_livre -= 1
            vencedor = self.verificaVencedor(jogador,microTabuleiro//3, microTabuleiro%3, self.tabuleiro)
            if vencedor:
                print(f'{jogador} ganhou o jogo!!!')
                return True
            elif self.espacos_livre == 0:
                print("Ninguém ganhou, o jogo deu velha! :/")
                return True