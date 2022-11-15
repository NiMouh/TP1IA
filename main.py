import math
import random
import socket
import sys

interactive_flag = False

depth_analysis = 3

# Declaração da valoração de cada uma das peças
pts = [50, 30, 30, 90, 900, 30, 30, 50, 10, 10, 10, 10, 10, 10, 10, 10]


def pos2_to_pos1(x2):
    return x2[0] * 8 + x2[1]


def pos1_to_pos2(x):
    row = x // 8
    col = x % 8
    return [row, col]


# Função posição começo do jogo, recebe uma peça a posição e o jogador
def position(piece, pos, play):
    # Declaração das tabelas de posição (priorizar jogo centralizado e peças avançadas)
    # Tabela de posições da rainha
    queen_table = [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
                   -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0,
                   -1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0,
                   -0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5,
                   0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5,
                   -1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0,
                   -1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0,
                   -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]

    # Tabela de posições do rei
    king_table = [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                  -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                  -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                  -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                  -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
                  -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
                  2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0,
                  2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]

    # Tabela de posições do cavalo para o início do jogo
    knight_table = [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
                    -4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0,
                    -3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0,
                    -3.0, 0.5, 1.5, 1.5, 1.5, 1.5, 0.5, -3.0,
                    -3.0, 0.0, 1.5, 1.5, 1.5, 1.5, 0.0, -3.0,
                    -3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0,
                    -4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0,
                    -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]

    # Tabela de posições do bispo
    bishop_table = [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
                    -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0,
                    -1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0,
                    -1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0,
                    -1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0,
                    -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0,
                    -1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0,
                    -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]

    # Tabela de posições da torre
    rook_table = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5,
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5,
                  0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]

    # Tabela de posições do peão
    pawn_table = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
                  1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0,
                  0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5,
                  0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0,
                  0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5,
                  0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # Se a peça for um cavalo ('a' e 'h')
    if piece == 'a' or piece == 'A' or piece == 'h' or piece == 'H':
        # Caso sejam as brancas
        if play == 1:
            # Retorna a pontuação da tabela de posição do cavalo (invertida)
            return list(reversed(knight_table))[pos]
        # Senão retorna a pontuação da tabela de posição do cavalo
        return knight_table[pos]

    # Se a peça for um bispo ('b' e 'g')
    elif piece == 'b' or piece == 'B' or piece == 'g' or piece == 'G':
        # Caso sejam as brancas
        if play == 1:
            # Retorna a pontuação da tabela da posição do bispo (invetida)
            return list(reversed(bishop_table))[pos]
        # Senão retorna a pontuação da tabela de posição do bispo
        return bishop_table[pos]

    # Se a peça for uma torre ('c' e 'f')
    elif piece == 'c' or piece == 'C' or piece == 'f' or piece == 'F':
        # Caso sejam as brancas
        if play == 1:
            # Retorna a pontuação da tabela de posição da torre (invertida)
            return list(reversed(rook_table))[pos]
        # Senão retorna a pontuação da tabela de posição da torre
        return rook_table[pos]

    # Se a peça for uma rainha ('d')
    elif piece == 'd' or piece == 'D':
        # Caso sejam as brancas
        if play == 1:
            # Retorna a pontuação da tabela de posição da rainha (invertida)
            return list(reversed(queen_table))[pos]
        # Senão retorna a pontuação da tabela de posição da rainha
        return queen_table[pos]

    # Se a peça for um rei ('e')
    elif piece == 'e' or piece == 'E':
        # Caso sejam as brancas
        if play == 1:
            # Retorna a pontuação da tabela de posição do rei (invertida)
            return list(reversed(king_table))[pos]
        # Senão retorna a pontuação da tabela de posição do rei
        return king_table[pos]

    # Se a peça for um peão (está entre i e p)
    else:
        # Caso sejam as brancas
        if play == 1:
            # Retorna a pontuação da tabela de posição do peão (invertida)
            return list(reversed(pawn_table))[pos]
        # Senão retorna a pontuação da tabela de posição do peão
        return pawn_table[pos]


# Função sobre ameaça ativa, recebe o tabuleiro e uma peça e retorna uma pontuação dado a quantidade que ela ameaça
def active_threat(board, piece):
    # Declaração das peças brancas e pretas em modo ‘string’
    # a, h = torres; b,g = cavalos; c,f =bispo; d= rainha; e = rei; restantes = peões
    w = 'abcdefghijklmnop'
    b = 'ABCDEFGHIJKLMNOP'

    # Conjunto de peças que podem ameaçar a peça
    res = []
    # Declaração da variável de posição da peça
    pos = board.find(piece)
    # Declaração da variável de posição da peça (2D)
    pos2 = pos1_to_pos2(pos)
    if piece == 'a' or piece == 'h':  # Torre branca
        # Ciclo que percorre o tabuleiro horizontalmente
        for i in range(1, 8):  # Norte
            if pos2[0] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1]))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Sul
            if pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1]))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Leste
            if pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Oeste
            if pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        return res
    elif piece == 'b' or piece == 'g':  # Cavalo branco
        # Ciclo que percorre o tabuleiro em L
        for i in range(1, 3):  # Nordeste
            if pos2[0] + i > 7 or pos2[1] + 3 - i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + 3 - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 3):  # Sudeste
            if pos2[0] - i < 0 or pos2[1] + 3 - i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + 3 - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 3):  # Sudoeste
            if pos2[0] - i < 0 or pos2[1] - 3 + i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - 3 + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 3):  # Noroeste
            if pos2[0] + i > 7 or pos2[1] - 3 + i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - 3 + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        return res
    elif piece == 'c' or piece == 'f':  # Bispo branco
        # Ciclo que percorre o tabuleiro diagonalmente
        for i in range(1, 8):  # Nordeste
            if pos2[0] + i > 7 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Sudeste
            if pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Sudoeste
            if pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Noroeste
            if pos2[0] + i > 7 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        return res
    elif piece == 'd':  # Rainha branca
        # Ciclo que percorre o tabuleiro em todas as direções
        for i in range(1, 8):  # Norte
            if pos2[0] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1]))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Sul
            if pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1]))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Leste
            if pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Oeste
            if pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Nordeste
            if pos2[0] + i > 7 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Sudeste
            if pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Sudoeste
            if pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 8):  # Noroeste
            if pos2[0] + i > 7 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        return res
    elif piece == 'e':  # Rei branco
        # Ciclo que percorre o tabuleiro em todas as direções
        for i in range(1, 2):  # Norte (1 casa)

            if pos2[0] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1]))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 2):  # Sul (1 casa)
            if pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1]))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 2):  # Leste (1 casa)
            if pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 2):  # Oeste (1 casa)
            if pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 2):  # Nordeste (1 casa)
            if pos2[0] + i > 7 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 2):  # Sudeste (1 casa)
            if pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 2):  # Sudoeste (1 casa)
            if pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        for i in range(1, 2):  # Noroeste (1 casa)
            if pos2[0] + i > 7 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - i))]  # Peça em ameaça
            if o in w or o == 'z':  # Ascii de 'a' a 'z'
                break
            elif o in b:
                res.append(o)
                break
        return res
    elif piece == 'A' or piece == 'H':  # Torre preta
        # Ciclo que percorre o tabuleiro em todas as direções
        for i in range(1, 8):  # Norte
            if pos2[0] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1]))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' a 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Sul
            if pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1]))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' a 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Leste
            if pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' a 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Oeste
            if pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' a 'z'
                break
            elif o in w:
                res.append(o)
                break
        return res
    elif piece == 'B' or piece == 'G':  # Cavalo preto
        # Ciclo que percorre o tabuleiro em todas as direções
        for i in range(1, 3):  # Norte
            if pos2[0] + i > 7:
                break
            for j in range(1, 3):
                if pos2[1] + j > 7:
                    break
                o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + j))]
                if o in b or o == 'z':  # Ascii de 'A' a 'Z' a 'z'
                    break
                elif o in w:
                    res.append(o)
                    break
        for i in range(1, 3):  # Sul
            if pos2[0] - i < 0:
                break
            for j in range(1, 3):
                if pos2[1] - j < 0:
                    break
                o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - j))]
                if o in b or o == 'z':  # Ascii de 'A' a 'Z' a 'z'
                    break
                elif o in w:
                    res.append(o)
                    break
        for i in range(1, 3):  # Leste
            if pos2[1] + i > 7:
                break
            for j in range(1, 3):
                if pos2[0] - j < 0:
                    break
                o = board[pos2_to_pos1((pos2[0] - j, pos2[1] + i))]
                if o in b or o == 'z':  # Ascii de 'A' a 'Z' a 'z'
                    break
                elif o in w:
                    res.append(o)
                    break
        for i in range(1, 3):  # Oeste
            if pos2[1] - i < 0:
                break
            for j in range(1, 3):
                if pos2[0] + j > 7:
                    break
                o = board[pos2_to_pos1((pos2[0] + j, pos2[1] - i))]
                if o in b or o == 'z':  # Ascii de 'A' a 'Z' a 'z'
                    break
                elif o in w:
                    res.append(o)
                    break
        return res
    elif piece == 'C' or piece == 'F':  # Bispo preto
        # Ciclo que percorre o tabuleiro em todas as direções
        for i in range(1, 8):  # Nordeste
            if pos2[0] + i > 7 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Sudeste
            if pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Sudoeste
            if pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Noroeste
            if pos2[0] + i > 7 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        return res
    elif piece == 'D':  # Rainha preta
        # Ciclo que percorre o tabuleiro em todas as direções
        for i in range(1, 8):  # Norte
            if pos2[0] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1]))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Sul
            if pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1]))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Leste
            if pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Oeste
            if pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Nordeste
            if pos2[0] + i > 7 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Sudeste
            if pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Sudoeste
            if pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 8):  # Noroeste
            if pos2[0] + i > 7 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        return res
    elif piece == 'E':  # Rei Preto
        # Ciclo que percorre o tabuleiro em todas as direções
        for i in range(1, 2):  # Norte
            if pos2[0] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1]))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 2):  # Sul
            if pos2[0] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1]))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 2):  # Leste
            if pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 2):  # Oeste
            if pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0], pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 2):  # Nordeste
            if pos2[0] + i > 7 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 2):  # Sudeste
            if pos2[0] - i < 0 or pos2[1] + i > 7:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] + i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 2):  # Sudoeste
            if pos2[0] - i < 0 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] - i, pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        for i in range(1, 2):  # Noroeste
            if pos2[0] + i > 7 or pos2[1] - i < 0:
                break
            o = board[pos2_to_pos1((pos2[0] + i, pos2[1] - i))]  # Peça em ameaça
            if o in b or o == 'z':  # Ascii de 'A' a 'Z' e 'z'
                break
            elif o in w:
                res.append(o)
                break
        return res

    # Caso não seja uma peça válida, retorna uma lista vazia
    return res


# Função sobre ameaça passiva, recebe o tabuleiro e uma peça e retorna uma pontuação dado a ameaça sofrida
def passive_threat(board, piece):
    # Declaração das peças brancas e pretas em modo ‘string’
    # a, h = torres; b,g = cavalos; c,f =bispo; d= rainha; e = rei; restantes = peões
    w = 'abcdefghijklmnop'
    b = 'ABCDEFGHIJKLMNOP'

    # Conjunto de peças que podem ameaçar a peça
    res = []
    # Declaração da variável de posição da peça
    pos = board.find(piece)
    # Declaração da variável de posição da peça (2D)
    pos2 = pos1_to_pos2(pos)

    # POR FAZER


# Função objetivo, recebe o estado atual e o qual jogador é que esta a ser jogado com
# (1 para as brancas 0 para as pretas)
def f_obj(board, play):
    # Declaração das peças brancas e pretas em modo ‘string’
    # a, h = torres; b,g = cavalos; c,f =bispo; d= rainha; e = rei; restantes = peões
    w = 'abcdefghijklmnop'
    b = 'ABCDEFGHIJKLMNOP'

    # Declaração da valoração de cada uma das peças
    global pts

    # Declaração da variavel que representa a pontuação obtida pelas peças brancas
    score_w = 0
    # Declaração da variavel que representa a quantos movimentos foram feitos pelas peças brancas
    score_w_positions = 0
    # Declaração da variavel que representa a quantidades de peças brancas a ameaçar
    score_w_threats = 0

    for i, p in enumerate(w):
        # Procura se o tabuleiro a analisar contêm essa peça
        ex = board.find(p)
        # Caso contenha
        if ex >= 0:
            # Aumenta a pontuação tendo em conta a valoração da peça dada na lista 'pts.'
            score_w += pts[i]
            # Aumenta a pontuação da posição dentro em conta o peso e a posição dela (eixo) dos x (do lado dos brancos)
            score_w_positions += position(p, ex, 1)
            # Declaração de variavel que guarda as peças em ameaça
            threats = active_threat(board, p)
            # Caso esteja a ameaçar o rei preto
            if 'D' in threats or 'E' in threats:
                # Aumenta a pontuação
                score_w_threats += 10
            # Caso esteja a ameaçar uma torre preta
            if 'A' in threats or 'H' in threats:
                # Aumenta a pontuação
                score_w_threats += 5
            # Caso esteja a ameaçar um bispo preto
            if 'C' in threats or 'F' in threats or 'B' in threats or 'G' in threats:
                # Aumenta a pontuação
                score_w_threats += 3

    # Declaração da variavel que representa a pontuação obtida pelas peças pretas
    score_b = 0
    # Declaração da variavel que representa a quantos movimentos foram feitos pelas peças pretas
    score_b_positions = 0
    # Declaração da variavel que representa a quantidades de peças pretas a ameaçar
    score_b_threats = 0
    for i, p in enumerate(b):
        # Procura se o tabuleiro a analisar contêm essa peça
        ex = board.find(p)
        # Caso contenha
        if ex >= 0:
            # Aumenta a pontuação tendo em conta a valoração da peça dada na lista 'pts.'
            score_b += pts[i]
            # Aumenta a pontuação da posição dentro em conta o peso e a posição dela (eixo) dos x (do lado dos pretos)
            score_b_positions += position(p, ex, 0)
            # Declaração de variavel que guarda as peças em ameaça
            threats = active_threat(board, p)
            # Caso esteja a ameaçar o rei branco
            if 'd' in threats or 'e' in threats:
                # Aumenta a pontuação
                score_b_threats += 10
            # Caso esteja a ameaçar uma torre branca
            if 'a' in threats or 'h' in threats:
                # Aumenta a pontuação
                score_b_threats += 5
            # Caso esteja a ameaçar um bispo branco
            if 'c' in threats or 'f' in threats or 'b' in threats or 'g' in threats:
                # Aumenta a pontuação
                score_b_threats += 3

    # Devolve a pontuação final como a diferença (tanto do número de peças como movimentos feitos)
    # entre as brancas e as pretas multiplicando por a variavel 'play' para determinar se é boa para nós ou má para nós
    # e se o jogador atual tem o melhor controlo do tabuleiro
    return (score_w + score_w_positions + score_w_threats - score_b - score_b_positions - score_b_threats) * pow(-1,
                                                                                                                 play)


# OPENINGS — Aberturas
# Priorizar movimentos onde o cavalo está no centro do tabuleiro e não na borda
# Priorizar manter o par de bispos
# Priorizar movimentos onde o jogo é centrado
# Priorizar movimentos onde o rei fica mais protegido e reforçado

# Priorizar movimentos onde as peças á frente do rei estão protegidas por mais alguma peça
# Fazer verificação se alguma peça está prestes a comer o rei,
# e colocar peças á frente do rei para proteger ou mexer o rei

# ENDGAME
# Favorece posições em que o rei adversário está perto do canto do tabuleiro
# Incentivar mover o rei perto do rei adversário (incrementar caso existam menos de 3 peças entre eles)


def find_node(tr, id):
    if len(tr) == 0:
        return None
    if tr[0] == id:
        return tr
    for t in tr[-1]:
        aux = find_node(t, id)
        if aux is not None:
            return aux
    return None


def get_positions_directions(state, piece, p2, directions):
    ret = []
    for d in directions:
        for r in range(1, d[1] + 1):
            if d[0] == 'N':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1]])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1]])
                break

            if d[0] == 'S':
                if p2[0] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1]])] == 'z':
                    ret.append([p2[0] + r, p2[1]])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1]])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1]])
                break
            if d[0] == 'W':
                if p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0], p2[1] - r])] == 'z':
                    ret.append([p2[0], p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0], p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0], p2[1] - r])
                break
            if d[0] == 'E':
                if p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0], p2[1] + r])] == 'z':
                    ret.append([p2[0], p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0], p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0], p2[1] + r])
                break
            if d[0] == 'NE':
                if p2[0] - r < 0 or p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1] + r])] == 'z':
                    ret.append([p2[0] - r, p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1] + r])
                break
            if d[0] == 'SW':
                if p2[0] + r > 7 or p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1] - r])] == 'z':
                    ret.append([p2[0] + r, p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1] - r])
                break
            if d[0] == 'NW':
                if p2[0] - r < 0 or p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1] - r])] == 'z':
                    ret.append([p2[0] - r, p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1] - r])
                break
            if d[0] == 'SE':
                if p2[0] + r > 7 or p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1] + r])] == 'z':
                    ret.append([p2[0] + r, p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1] + r])
                break
            if d[0] == 'PS':
                if p2[0] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1]])] == 'z':
                    ret.append([p2[0] + r, p2[1]])
                    continue
                break
            if d[0] == 'PN':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                    continue
                break
            if d[0] == 'PS2':
                if p2[0] + r <= 7 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] + r, p2[1] + 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] + 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] + r, p2[1] + 1])

                if p2[0] + r <= 7 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] + r, p2[1] - 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] - 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] + r, p2[1] - 1])
                continue
            if d[0] == 'PN2':
                if p2[0] - r >= 0 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] - r, p2[1] + 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] + 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] - r, p2[1] + 1])

                if p2[0] - r >= 0 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] - r, p2[1] - 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] - 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] - r, p2[1] - 1])
                continue
            if d[0] == 'H':
                if p2[0] - 2 >= 0 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] - 2, p2[1] - 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 2, p2[1] - 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 2, p2[1] - 1])

                if p2[0] - 2 >= 0 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] - 2, p2[1] + 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 2, p2[1] + 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 2, p2[1] + 1])

                if p2[0] - 1 >= 0 and p2[1] + 2 <= 7:
                    if state[pos2_to_pos1([p2[0] - 1, p2[1] + 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 1, p2[1] + 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 1, p2[1] + 2])

                if p2[0] + 1 <= 7 and p2[1] + 2 <= 7:
                    if state[pos2_to_pos1([p2[0] + 1, p2[1] + 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 1, p2[1] + 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 1, p2[1] + 2])

                if p2[0] + 2 <= 7 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] + 2, p2[1] + 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 2, p2[1] + 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 2, p2[1] + 1])

                if p2[0] + 2 <= 7 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] + 2, p2[1] - 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 2, p2[1] - 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 2, p2[1] - 1])

                if p2[0] + 1 <= 7 and p2[1] - 2 >= 0:
                    if state[pos2_to_pos1([p2[0] + 1, p2[1] - 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 1, p2[1] - 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 1, p2[1] - 2])

                if p2[0] - 1 >= 0 and p2[1] - 2 >= 0:
                    if state[pos2_to_pos1([p2[0] - 1, p2[1] - 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 1, p2[1] - 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 1, p2[1] - 2])
    return ret


def count_nodes(tr):
    ret = 0
    if len(tr) > 0:
        for t in tr[-1]:
            ret += count_nodes(t)
        return 1 + ret
    return ret


def get_available_positions(state, p2, piece):
    ret = []
    if piece in ('a', 'h', 'A', 'H'):  # Tower
        aux = get_positions_directions(state, piece, p2, [['N', 7], ['S', 7], ['W', 7], ['E', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('c', 'f', 'C', 'F'):  # Bishop
        aux = get_positions_directions(state, piece, p2, [['NE', 7], ['SE', 7], ['NW', 7], ['SW', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('d', 'D'):  # Queen
        aux = get_positions_directions(state, piece, p2,
                                       [['N', 7], ['S', 7], ['W', 7], ['E', 7], ['NE', 7], ['SE', 7], ['NW', 7],
                                        ['SW', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('e', 'E'):  # King
        aux = get_positions_directions(state, piece, p2,
                                       [['N', 1], ['S', 1], ['W', 1], ['E', 1], ['NE', 1], ['SE', 1], ['NW', 1],
                                        ['SW', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('b', 'g', 'B', 'G'):  # Horse
        aux = get_positions_directions(state, piece, p2, [['H', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    # Pawn
    if ord('i') <= ord(piece) <= ord('p'):
        if p2[0] == 1:
            aux = get_positions_directions(state, piece, p2, [['PS', 2]])
            if len(aux) > 0:
                ret.extend(aux)
        else:
            aux = get_positions_directions(state, piece, p2, [['PS', 1]])
            if len(aux) > 0:
                ret.extend(aux)
        aux = get_positions_directions(state, piece, p2, [['PS2', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if ord('I') <= ord(piece) <= ord('P'):
        if p2[0] == 6:
            aux = get_positions_directions(state, piece, p2, [['PN', 2]])
            if len(aux) > 0:
                ret.extend(aux)
        else:
            aux = get_positions_directions(state, piece, p2, [['PN', 1]])
            if len(aux) > 0:
                ret.extend(aux)
        aux = get_positions_directions(state, piece, p2, [['PN2', 1]])
        if len(aux) > 0:
            ret.extend(aux)
    return ret


def find_all(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def sucessor_states(state, player):
    ret = []

    for x in range(ord('a') - player * 32, ord('p') - player * 32 + 1):

        p_all = find_all(state, chr(x))

        if len(p_all) == 0:
            continue

        for p in p_all:
            p2 = pos1_to_pos2(p)

            pos_available = get_available_positions(state, p2, chr(x))

            for a in pos_available:
                state_aux = list('%s' % state)
                state_aux[p] = 'z'
                if ord('i') <= x <= ord('p') and a[0] == 7:
                    state_aux[pos2_to_pos1(a)] = 'd'
                elif ord('I') <= x <= ord('P') and a[0] == 0:
                    state_aux[pos2_to_pos1(a)] = 'D'
                else:
                    state_aux[pos2_to_pos1(a)] = chr(x)
                ret.append(''.join(state_aux))

    return ret


def insert_state_tree(tr, nv, parent):
    nd = find_node(tr, parent[0])
    if nd is None:
        return None
    nd[-1].append(nv)
    return tr


def get_description_piece(piece):
    if ord(piece) < 97:
        ret = 'Black '
    else:
        ret = 'White '
    if piece.lower() in ('a', 'h'):
        ret = ret + 'Tower'
    elif piece.lower() in ('b', 'g'):
        ret = ret + 'Horse'
    elif piece.lower() in ('c', 'f'):
        ret = ret + 'Bishop'
    elif piece.lower() == 'd':
        ret = ret + 'Queen'
    elif piece.lower() == 'e':
        ret = ret + 'King'
    else:
        ret = ret + 'Pawn'
    return ret


def description_move(prev, cur, idx, nick):
    # print('description_move()')
    ret = 'Move [%d - %s]: ' % (idx, nick)

    cur_blank = [i for i, ltr in enumerate(cur) if ltr == 'z']
    prev_not_blank = [i for i, ltr in enumerate(prev) if ltr != 'z']

    moved = list(set(cur_blank) & set(prev_not_blank))

    moved = moved[0]

    desc_piece = get_description_piece(prev[moved])

    fr = pos1_to_pos2(moved)
    to = pos1_to_pos2(cur.find(prev[moved]))

    ret = ret + desc_piece + ' (%d, %d) --> (%d, %d)' % (fr[0], fr[1], to[0], to[1])
    if prev[pos2_to_pos1(to)] != 'z':
        desc_piece = get_description_piece(prev[pos2_to_pos1(to)])
        ret = ret + ' eaten ' + desc_piece
    return ret


def expand_tree(tr, dep, n, play):
    if n == 0:
        return tr
    suc = sucessor_states(tr[0], play)
    for s in suc:
        tr = insert_state_tree(tr, expand_tree([s, random.random(), dep + 1, 0, f_obj(s, play), []], dep + 1, n - 1,
                                               1 - play), tr)
    return tr


def get_father(tr, st):
    if len(tr) == 0:
        return None
    for sun in tr[-1]:
        if sun[1] == st[1]:
            return tr

    for sun in tr[-1]:
        aux = get_father(sun, st)
        if aux is not None:
            return aux

    return None


def get_next_move(tree, st):
    old = None
    while get_father(tree, st) is not None:
        old = st
        st = get_father(tree, st)
    return old


def minimax_alpha_beta(tr, d, play, max_player, alpha, beta):
    if d == 0 or len(tr[-1]) == 0:
        return tr, f_obj(tr[0], play)

    ret = math.inf * pow(-1, max_player)
    ret_nd = tr
    for s in tr[-1]:
        aux, val = minimax_alpha_beta(s, d - 1, play, not max_player, alpha, beta)
        if max_player:
            if val > ret:
                ret = val
                ret_nd = aux
            alpha = max(alpha, ret)
        else:
            if val < ret:
                ret = val
                ret_nd = aux
            beta = min(beta, ret)
        if beta <= alpha:
            break

    return ret_nd, ret


def decide_move(board, play, nick):
    states = expand_tree([board, random.random(), 0, f_obj(board, play), []], 0, depth_analysis,
                         play)  # [board, hash, depth, g(), f_obj(), [SUNS]]

    print('Total nodes in the tree: %d' % count_nodes(states))

    choice, value = minimax_alpha_beta(states, depth_analysis, play, True, -math.inf, math.inf)

    next_move = get_next_move(states, choice)

    return next_move[0]


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect((sys.argv[1], int(sys.argv[2])))  # connecting client to server

hello_msg = '%s_%s' % (sys.argv[4], sys.argv[3])
client.send(hello_msg.encode('ascii'))

nickname = sys.argv[3]

player = int(sys.argv[4])

while True:  # making valid connection
    while True:
        message = client.recv(1024).decode('ascii')
        if len(message) > 0:
            break

    if interactive_flag:
        row_from = int(input('Row from > '))
        col_from = int(input('Col from > '))
        row_to = int(input('Row to > '))
        col_to = int(input('Col to > '))

        p_from = pos2_to_pos1([row_from, col_from])
        p_to = pos2_to_pos1([row_to, col_to])

        if (0 <= p_from <= 63) and (0 <= p_to <= 63):
            message = list(message)
            aux = message[p_from]
            message[p_from] = 'z'
            message[p_to] = aux
            message = ''.join(message)
    else:
        message = decide_move(message, player, nickname)

    client.send(message.encode('ascii'))
