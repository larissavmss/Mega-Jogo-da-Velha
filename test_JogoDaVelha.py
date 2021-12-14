#!/usr/bin/env python3.8.10
# -*- coding: utf-8 -*-

import pytest
from JogoDaVelha import *


@pytest.mark.parametrize("linhas, colunas, resultado", [([0,1,0,0,2,1,1,2,2],[0,1,1,2,0,0,2,1,2],"V"),
([2,2,0,1,0,0,1,1,2],[2,0,0,1,2,1,2,0,1],"X"), ([1,0,2,0,2,0,1],[1,0,0,2,1,1,2],"O"),([1,1,2,0,2,2,0],[1,0,0,2,2,1,0],"X"),
([2,0,1,0,0,2,1,1,2],[1,0,1,1,2,0,0,2,2],"V"),([0,0,1,2,1,1],[2,0,0,2,2,1],"O")])

class TestaMicroTabuleiro:
    def test_jogoNoMicroTabuleiro(self, linhas, colunas, resultado):
        micro = TabuleiroMicro()
        i = 0
        while micro.vencedor == None:
            if i%2 == 0:
                micro.marcaQuadrado(linhas[i],colunas[i], "X")
            else:
                micro.marcaQuadrado(linhas[i],colunas[i], "O")
            i +=1
        assert micro.vencedor == resultado

@pytest.mark.parametrize("microTab, resultado", [([4,7,5,3,6,2,0,8,1],None),([0,6,5,2,4,3,8],"X"),([0,4,2,1,7,8,6,3,5], None),
([3,7,5,4,1,8,0,6],"O"),([2,3,8,5,4,6,0],"X"), ([4,5,7,1,3,2,8,0],"O")])
class TestaMacroTabuleiro:
    def test_jogada(self, microTab, resultado):
        macro = TabuleiroMacro()
        k = i=0
        while not(macro.fimDeJogo):
            if k%2==0:
                jogador = "X"
            else:
                jogador = "O"
            for i in range(3): #Como já testamos o micro-tabuleiro vamos apenas marcar eles focando no macro
                macro.jogada(microTab[k],jogador ,i, i)
            k+=1
        assert macro.vencedor == resultado

class TestaEscolhePosicao:
    @pytest.mark.parametrize("repeticoes", [1,2,3,4,5,6,7,8,9,10])
    def test_JogadorEstabanado(self, repeticoes):
        tabuleiro = TabuleiroMacro()
        jogador = JogadorEstabanado("Larissa", "X")
        while not(tabuleiro.fimDeJogo):
            jogador.escolhePosicao(tabuleiro)
        assert tabuleiro.vencedor == "X"

    def test_JogadorComeCru(self):
        tabuleiro = TabuleiroMacro()
        jogador = JogadorComeCru("Larissa","X")
        while not(tabuleiro.fimDeJogo):
            jogador.escolhePosicao(tabuleiro)
        assert tabuleiro.tabuleiro[0][0].vencedor == tabuleiro.tabuleiro[0][1].vencedor== tabuleiro.tabuleiro[0][2].vencedor == "X"
        
class TestaMain:
    def test_jogoHH(self):

    def test_jogoHE(self):
    
    def test_jogoEE(self):