import math
import random
import socket
import sys

interactive_flag = False

depth_analysis = 3

# Declaração da valoração de cada uma das peças
pts = [100, 70, 60, 1000, 9999, 60, 70, 100, 10, 10, 10, 10, 10, 10, 10, 10]

# Declara uma variavel global que define o end_game
end_game_material = 1 * pts[0] + 1 * pts[1] + 2 * pts[2] + 1 * pts[3] + 1 * pts[4]


def pos2_to_pos1(x2):
    return x2[0] * 8 + x2[1]


def pos1_to_pos2(x):
    row = x // 8
    col = x % 8
    return [row, col]


# Função posição começo do jogo, recebe uma peça a posição e o jogador
def position_start(piece, pos, play):
    # Declaração das tabelas de posição (priorizar jogo centralizado e peças avançadas)
    # Tabela de posição dos peões para o início do jogo
    pawn_table = [0, 0, 0, 0, 0, 0, 0, 0,
                  50, 50, 50, 50, 50, 50, 50, 50,
                  10, 10, 20, 30, 30, 20, 10, 10,
                  5, 5, 15, 25, 25, 15, 5, 5,
                  0, 0, 0, 40, 40, 0, 0, 0,
                  5, -5, -10, 0, 0, -10, -5, 5,
                  5, 10, 10, -20, -20, 10, 10, 5,
                  0, 0, 0, 0, 0, 0, 0, 0]
    # Tabela de posição dos cavalos
    knight_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                    -40, -20, 0, 0, 0, 0, -20, -40,
                    -30, 0, 10, 15, 15, 10, 0, -30,
                    -30, 5, 15, 20, 20, 15, 5, -30,
                    -30, 0, 15, 20, 20, 15, 0, -30,
                    -30, 5, 10, 15, 15, 10, 5, -30,
                    -40, -20, 0, 5, 5, 0, -20, -40,
                    -50, -40, -30, -30, -30, -30, -40, -50]
    # Tabela de posição dos bispos
    bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                    -10, 0, 0, 0, 0, 0, 0, -10,
                    -10, 0, 5, 10, 10, 5, 0, -10,
                    -10, 5, 5, 10, 10, 5, 5, -10,
                    -10, 0, 10, 10, 10, 10, 0, -10,
                    -10, 10, 10, 10, 10, 10, 10, -10,
                    -10, 5, 0, 0, 0, 0, 5, -10,
                    -20, -10, -10, -10, -10, -10, -10, -20]
    # Tabela de posição das torres
    rook_table = [0, 0, 0, 0, 0, 0, 0, 0,
                  5, 10, 10, 10, 10, 10, 10, 5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  0, 0, 0, 5, 5, 0, 0, 0]
    # Tabela de posição da rainha
    queen_table = [-20, -10, -10, -5, -5, -10, -10, -20,
                   -10, 0, 0, 0, 0, 0, 0, -10,
                   -10, 0, 5, 5, 5, 5, 0, -10,
                   -5, 0, 5, 5, 5, 5, 0, -5,
                   0, 0, 5, 5, 5, 5, 0, -5,
                   -10, 5, 5, 5, 5, 5, 0, -10,
                   -10, 0, 5, 0, 0, 0, 0, -10,
                   -20, -10, -10, -5, -5, -10, -10, -20]
    # Tabela de posição do rei
    king_table = [-30, -40, -40, -50, -50, -40, -40, -30,
                  -30, -40, -40, -50, -50, -40, -40, -30,
                  -30, -40, -40, -50, -50, -40, -40, -30,
                  -30, -40, -40, -50, -50, -40, -40, -30,
                  -20, -30, -30, -40, -40, -30, -30, -20,
                  -10, -20, -20, -20, -20, -20, -20, -10,
                  20, 20, 0, 0, 0, 0, 20, 20,
                  20, 30, 10, 0, 0, 10, 30, 20]
    # Se a peça for um peão (está entre i e p)
    if piece == 'i' or piece == 'I' or piece == 'j' or piece == 'J' or piece == 'k' or piece == 'K' or piece == 'l' or piece == 'L' or piece == 'm' or piece == 'M' or piece == 'n' or piece == 'N' or piece == 'o' or piece == 'O' or piece == 'p' or piece == 'P':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do peão
            return pawn_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do peão invertida
            return pawn_table[63 - pos]
    # Se a peça for um cavalo ('a' e 'h')
    elif piece == 'a' or piece == 'A' or piece == 'h' or piece == 'H':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do cavalo
            return knight_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do cavalo invertida
            return knight_table[63 - pos]
    # Se a peça for um bispo ('b' e 'g')
    elif piece == 'b' or piece == 'B' or piece == 'g' or piece == 'G':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do bispo
            return bishop_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do bispo invertida
            return bishop_table[63 - pos]
    # Se a peça for uma torre ('c' e 'f')
    elif piece == 'c' or piece == 'C' or piece == 'f' or piece == 'F':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição da torre
            return rook_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição da torre invertida
            return rook_table[63 - pos]
    # Se a peça for uma rainha ('d')
    elif piece == 'd' or piece == 'D':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição da rainha
            return queen_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição da rainha invertida
            return queen_table[63 - pos]
    # Se a peça for um rei ('e')
    elif piece == 'e' or piece == 'E':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do rei
            return king_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do rei invertida
            return king_table[63 - pos]


# Função posição meio do jogo, recebe uma peça e a posição da mesma e o jogador
def position_mid(piece, pos, play):
    # Declaração das tabelas de posição do meio do jogo (priorizar o centro do tabuleiro e defender as peças)
    # Tabela de posição dos peões a meio do jogo
    pawn_table = [0, 0, 0, 0, 0, 0, 0, 0,
                  50, 50, 50, 50, 50, 50, 50, 50,
                  10, 10, 20, 30, 30, 20, 10, 10,
                  5, 5, 15, 25, 25, 15, 5, 5,
                  0, 0, 0, 30, 30, 0, 0, 0,
                  5, -5, -10, 0, 0, -10, -5, 5,
                  5, 10, 10, -20, -20, 10, 10, 5,
                  0, 0, 0, 0, 0, 0, 0, 0]
    # Tabela de posição dos cavalos
    knight_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                    -40, -20, 0, 0, 0, 0, -20, -40,
                    -30, 0, 10, 15, 15, 10, 0, -30,
                    -30, 5, 15, 20, 20, 15, 5, -30,
                    -30, 0, 15, 20, 20, 15, 0, -30,
                    -30, 5, 10, 15, 15, 10, 5, -30,
                    -40, -20, 0, 5, 5, 0, -20, -40,
                    -50, -40, -30, -30, -30, -30, -40, -50]
    # Tabela de posição dos bispos
    bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                    -10, 0, 0, 0, 0, 0, 0, -10,
                    -10, 0, 5, 10, 10, 5, 0, -10,
                    -10, 5, 5, 10, 10, 5, 5, -10,
                    -10, 0, 10, 10, 10, 10, 0, -10,
                    -10, 10, 10, 10, 10, 10, 10, -10,
                    -10, 5, 0, 0, 0, 0, 5, -10,
                    -20, -10, -10, -10, -10, -10, -10, -20]
    # Tabela de posição das torres
    rook_table = [0, 0, 0, 0, 0, 0, 0, 0,
                  5, 10, 10, 10, 10, 10, 10, 5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  0, 0, 0, 5, 5, 0, 0, 0]
    # Tabela de posição da rainha
    queen_table = [-20, -10, -10, -5, -5, -10, -10, -20,
                   -10, 0, 0, 0, 0, 0, 0, -10,
                   -10, 0, 5, 5, 5, 5, 0, -10,
                   -5, 0, 5, 5, 5, 5, 0, -5,
                   0, 0, 5, 5, 5, 5, 0, -5,
                   -10, 5, 5, 5, 5, 5, 0, -10,
                   -10, 0, 5, 0, 0, 0, 0, -10,
                   -20, -10, -10, -5, -5, -10, -10, -20]
    # Tabela de posição do rei
    king_table = [-30, -40, -40, -50, -50, -40, -40, -30,
                  -30, -40, -40, -50, -50, -40, -40, -30,
                  -30, -40, -40, -50, -50, -40, -40, -30,
                  -30, -40, -40, -50, -50, -40, -40, -30,
                  -20, -30, -30, -40, -40, -30, -30, -20,
                  -10, -20, -20, -20, -20, -20, -20, -10,
                  20, 20, 0, 0, 0, 0, 20, 20,
                  20, 30, 10, 0, 0, 10, 30, 20]
    # Se a peça for um peão (está entre i e p)
    if piece == 'i' or piece == 'I' or piece == 'j' or piece == 'J' or piece == 'k' or piece == 'K' or piece == 'l' or piece == 'L' or piece == 'm' or piece == 'M' or piece == 'n' or piece == 'N' or piece == 'o' or piece == 'O' or piece == 'p' or piece == 'P':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do peão
            return pawn_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do peão invertida
            return pawn_table[63 - pos]
    # Se a peça for um cavalo ('a' e 'h')
    elif piece == 'a' or piece == 'A' or piece == 'h' or piece == 'H':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do cavalo
            return knight_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do cavalo invertida
            return knight_table[63 - pos]
    # Se a peça for um bispo ('b' e 'g')
    elif piece == 'b' or piece == 'B' or piece == 'g' or piece == 'G':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do bispo
            return bishop_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do bispo invertida
            return bishop_table[63 - pos]
    # Se a peça for uma torre ('c' e 'f')
    elif piece == 'c' or piece == 'C' or piece == 'f' or piece == 'F':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição da torre
            return rook_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição da torre invertida
            return rook_table[63 - pos]
    # Se a peça for uma rainha ('d')
    elif piece == 'd' or piece == 'D':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição da rainha
            return queen_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição da rainha invertida
            return queen_table[63 - pos]
    # Se a peça for um rei ('e')
    elif piece == 'e' or piece == 'E':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do rei
            return king_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do rei invertida
            return king_table[63 - pos]


# Função posição fim do jogo, recebe uma peça e a posição da mesma e o jogador
def position_end(piece, pos, play):
    # Declaração das tabelas de posição do meio do jogo (priorizar defesa do rei e capturas)
    # Tabela de posição do peão no fim de jogo
    pawn_end_table = [0, 0, 0, 0, 0, 0, 0, 0,
                      5, 10, 10, -20, -20, 10, 10, 5,
                      5, -5, -10, 0, 0, -10, -5, 5,
                      0, 0, 0, 20, 20, 0, 0, 0,
                      5, 5, 10, 25, 25, 10, 5, 5,
                      10, 10, 20, 30, 30, 20, 10, 10,
                      50, 50, 50, 50, 50, 50, 50, 50,
                      0, 0, 0, 0, 0, 0, 0, 0]
    # Tabela de posição do cavalo no fim de jogo
    knight_end_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                        -40, -20, 0, 0, 0, 0, -20, -40,
                        -30, 0, 10, 15, 15, 10, 0, -30,
                        -30, 5, 15, 20, 20, 15, 5, -30,
                        -30, 0, 15, 20, 20, 15, 0, -30,
                        -30, 5, 10, 15, 15, 10, 5, -30,
                        -40, -20, 0, 5, 5, 0, -20, -40,
                        -50, -40, -30, -30, -30, -30, -40, -50]
    # Tabela de posição do bispo no fim de jogo
    bishop_end_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                        -10, 0, 0, 0, 0, 0, 0, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -10, 5, 5, 10, 10, 5, 5, -10,
                        -10, 0, 10, 10, 10, 10, 0, -10,
                        -10, 10, 10, 10, 10, 10, 10, -10,
                        -10, 5, 0, 0, 0, 0, 5, -10,
                        -20, -10, -10, -10, -10, -10, -10, -20]
    # Tabela de posição da torre no fim de jogo
    rook_end_table = [0, 0, 0, 0, 0, 0, 0, 0,
                      5, 10, 10, 10, 10, 10, 10, 5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      0, 0, 0, 5, 5, 0, 0, 0]
    # Tabela de posição da rainha no fim de jogo
    queen_end_table = [-20, -10, -10, -5, -5, -10, -10, -20,
                       -10, 0, 0, 0, 0, 0, 0, -10,
                       -10, 0, 5, 5, 5, 5, 0, -10,
                       -5, 0, 5, 5, 5, 5, 0, -5,
                       0, 0, 5, 5, 5, 5, 0, -5,
                       -10, 5, 5, 5, 5, 5, 0, -10,
                       -10, 0, 5, 0, 0, 0, 0, -10,
                       -20, -10, -10, -5, -5, -10, -10, -20]
    # Se a peça for um peão (está entre i e p)
    if piece == 'i' or piece == 'I' or piece == 'j' or piece == 'J' or piece == 'k' or piece == 'K' or piece == 'l' or piece == 'L' or piece == 'm' or piece == 'M' or piece == 'n' or piece == 'N' or piece == 'o' or piece == 'O' or piece == 'p' or piece == 'P':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do peão
            return pawn_end_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do peão invertida
            return pawn_end_table[63 - pos]
    # Se a peça for um cavalo ('a' e 'h')
    elif piece == 'a' or piece == 'A' or piece == 'h' or piece == 'H':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do cavalo
            return knight_end_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do cavalo invertida
            return knight_end_table[63 - pos]
    # Se a peça for um bispo ('b' e 'g')
    elif piece == 'b' or piece == 'B' or piece == 'g' or piece == 'G':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do bispo
            return bishop_end_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do bispo invertida
            return bishop_end_table[63 - pos]
    # Se a peça for uma torre ('c' e 'f')
    elif piece == 'c' or piece == 'C' or piece == 'f' or piece == 'F':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição da torre
            return rook_end_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição da torre invertida
            return rook_end_table[63 - pos]
    # Se a peça for uma rainha ('d')
    elif piece == 'd' or piece == 'D':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição da rainha
            return queen_end_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição da rainha invertida
            return queen_end_table[63 - pos]
    # Se a peça for um rei ('e')
    elif piece == 'e' or piece == 'E':
        # Se a peça for branca
        if play:
            # Retorna a pontuação da tabela de posição do rei
            return knight_end_table[pos]
        # Se a peça for preta
        else:
            # Retorna a pontuação da tabela de posição do rei invertida
            return knight_end_table[63 - pos]


# Função posição, recebe uma peça, a posição em que se encontra,
# se é branca ou preta e se é o fim de jogo, meio de jogo ou início de jogo
# e retorna uma pontuação conforme a posição da peça
def position(piece, pos, play, game_phase):
    # Se for o começo do jogo
    if game_phase == 0:
        # Retorna a pontuação da posição da peça
        return position_start(piece, pos, play)
    # Se for o meio do jogo
    elif game_phase == 1:
        # Retorna a pontuação da posição da peça
        return position_mid(piece, pos, play)
    # Se for o fim do jogo
    elif game_phase == 2:
        # Retorna a pontuação da posição da peça
        return position_end(piece, pos, play)


# Função sobre ameaça, recebe o tabuleiro e uma peça e retorna uma pontuação dado o quão ameaçada ela está
def threat(board, piece):
    res = []
    pos = board.find(piece)
    pos2 = pos1_to_pos2(pos)
    # Se for uma torre branca
    if piece == 'a' or piece == 'h':
        for i in range(1, pos2[0] + 8):  # Norte
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1]])]  # Peça ameaçada
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, 8 - pos2[0]):  # Sul
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1]])]  # Peça ameaçada
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, pos2[1] + 8):  # Oeste
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1] - i])]  # Peça ameaçada
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, 8 - pos2[1]):  # Leste
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1] + i])]  # Peça ameaçada
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
    # Se for uma torre preta
    elif piece == 'A' or piece == 'H':
        for i in range(1, pos2[0] + 8):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1]])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, 8 - pos2[0]):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1]])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, pos2[1] + 8):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1] - i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, 8 - pos2[1]):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1] + i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
    # Se for um bispo branco
    elif piece == 'c' or piece == 'f':
        for i in range(1, min(pos2[0] + 8, pos2[1] + 8)):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1] - i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, min(8 - pos2[0], pos2[1] + 8)):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1] - i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, min(pos2[0] + 8, 8 - pos2[1])):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1] + i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, min(8 - pos2[0], 8 - pos2[1])):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1] + i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
    # Se for um bispo preto
    elif piece == 'C' or piece == 'F':
        for i in range(1, min(pos2[0] + 8, pos2[1] + 8)):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1] - i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, min(8 - pos2[0], pos2[1] + 8)):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1] - i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, min(pos2[0] + 8, 8 - pos2[1])):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1] + i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, min(8 - pos2[0], 8 - pos2[1])):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1] + i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
    # Se for um cavalo branco
    elif piece == 'b' or piece == 'g':
        for i in range(1, 3):
            for j in range(1, 3):
                if i != j:
                    if 0 <= pos2[0] - i < 8 and 0 <= pos2[1] - j < 8:
                        o = board[pos2_to_pos1([pos2[0] - i, pos2[1] - j])]
                        # se 'o' estiver entre 'A' e 'Z'
                        if 'A' <= o <= 'Z':
                            res.append(o)
                    if 0 <= pos2[0] - i < 8 and 0 <= pos2[1] + j < 8:
                        o = board[pos2_to_pos1([pos2[0] - i, pos2[1] + j])]
                        # se 'o' estiver entre 'A' e 'Z'
                        if 'A' <= o <= 'Z':
                            res.append(o)
                    if 0 <= pos2[0] + i < 8 and 0 <= pos2[1] - j < 8:
                        o = board[pos2_to_pos1([pos2[0] + i, pos2[1] - j])]
                        # se 'o' estiver entre 'A' e 'Z'
                        if 'A' <= o <= 'Z':
                            res.append(o)
                    if 0 <= pos2[0] + i < 8 and 0 <= pos2[1] + j < 8:
                        o = board[pos2_to_pos1([pos2[0] + i, pos2[1] + j])]
                        # se 'o' estiver entre 'A' e 'Z'
                        if 'A' <= o <= 'Z':
                            res.append(o)
    # Se for um cavalo preto
    elif piece == 'B' or piece == 'G':
        for i in range(1, 3):
            for j in range(1, 3):
                if i != j:
                    if 0 <= pos2[0] - i < 8 and 0 <= pos2[1] - j < 8:
                        o = board[pos2_to_pos1([pos2[0] - i, pos2[1] - j])]
                        # se 'o' estiver entre 'a' e 'z'
                        if 'a' <= o <= 'z':
                            res.append(o)
                    if 0 <= pos2[0] - i < 8 and 0 <= pos2[1] + j < 8:
                        o = board[pos2_to_pos1([pos2[0] - i, pos2[1] + j])]
                        # se 'o' estiver entre 'a' e 'z'
                        if 'a' <= o <= 'z':
                            res.append(o)
                    if 0 <= pos2[0] + i < 8 and 0 <= pos2[1] - j < 8:
                        o = board[pos2_to_pos1([pos2[0] + i, pos2[1] - j])]
                        # se 'o' estiver entre 'a' e 'z'
                        if 'a' <= o <= 'z':
                            res.append(o)
                    if 0 <= pos2[0] + i < 8 and 0 <= pos2[1] + j < 8:
                        o = board[pos2_to_pos1([pos2[0] + i, pos2[1] + j])]
                        # se 'o' estiver entre 'a' e 'z'
                        if 'a' <= o <= 'z':
                            res.append(o)
    # Se for um rei branco
    elif piece == 'e':
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if 0 <= pos2[0] + i < 8 and 0 <= pos2[1] + j < 8:
                        o = board[pos2_to_pos1([pos2[0] + i, pos2[1] + j])]
                        # se 'o' estiver entre 'A' e 'Z'
                        if 'A' <= o <= 'Z':
                            res.append(o)
    # Se for um rei preto
    elif piece == 'E':
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if 0 <= pos2[0] + i < 8 and 0 <= pos2[1] + j < 8:
                        o = board[pos2_to_pos1([pos2[0] + i, pos2[1] + j])]
                        # se 'o' estiver entre 'a' e 'z'
                        if 'a' <= o <= 'z':
                            res.append(o)
    # Se for uma rainha branca
    elif piece == 'd':
        for i in range(1, pos2[0] + 8):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1]])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, 8 - pos2[0]):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1]])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, pos2[1] + 8):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1] - i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, 8 - pos2[1]):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1] + i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, min(pos2[0] + 8, pos2[1] + 8)):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1] - i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, min(8 - pos2[0], pos2[1] + 8)):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1] - i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, min(pos2[0] + 8, 8 - pos2[1])):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1] + i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
        for i in range(1, min(8 - pos2[0], 8 - pos2[1])):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1] + i])]
            # se 'o' estiver entre 'A' e 'Z'
            if 'A' <= o <= 'Z':
                res.append(o)
                break
    # Se for uma rainha preta
    elif piece == 'D':
        for i in range(1, pos2[0] + 8):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1]])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, 8 - pos2[0]):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1]])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, pos2[1] + 8):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1] - i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, 8 - pos2[1]):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0], pos2[1] + i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, min(pos2[0] + 8, pos2[1] + 8)):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1] - i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, min(8 - pos2[0], pos2[1] + 8)):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1] - i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, min(pos2[0] + 8, 8 - pos2[1])):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] - i, pos2[1] + i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
        for i in range(1, min(8 - pos2[0], 8 - pos2[1])):
            if i < 8:
                break
            o = board[pos2_to_pos1([pos2[0] + i, pos2[1] + i])]
            # se 'o' estiver entre 'a' e 'z'
            if 'a' <= o <= 'z':
                res.append(o)
                break
    return res


# Função objetivo, recebe o estado atual e o qual jogador é que esta a ser jogado com
# (1 para as brancas 0 para as pretas)
def f_obj(board, play):
    # Declaração das peças brancas e pretas em modo ‘string’
    # a, h = torres; b,g = cavalos; c,f =bispo; d= rainha; e = rei; restantes = peões
    w = 'abcdedghijklmnop'
    b = 'ABCDEFGHIJKLMNOP'
    # Declaração da valoração de cada uma das peças
    global pts
    # Declaração da variavel que representa a pontuação obtida pelas peças brancas
    score_w = 0
    # Declaração da variavel que representa a quantos movimentos foram feitos pelas peças brancas
    score_w_positions = 0

    # Se nenhuma peça for comida, em 10 jogadas, jogar agressivo
    conta = 64 - board.count('z')

    if conta == 64:
        weight_positions = 1e-3
    else:
        # Caso contrário, jogar defensivo
        weight_positions = 1e-1

    # Caso estejamos no fim do jogo
    if conta < 10:
        game_phase = 2
    elif conta < 20:
        game_phase = 1
    else:
        game_phase = 0

    for i, p in enumerate(w):
        # Procura se o tabuleiro a analisar contêm essa peça
        ex = board.find(p)
        # Caso contenha
        if ex >= 0:
            # Aumenta a pontuação tendo em conta a valoração da peça dada na lista 'pts.'
            score_w += pts[i]
            # Aumenta a pontuação da posição dentro em conta o peso e a posição dela (eixo) dos x (do lado dos brancos)
            score_w_positions += position(p, ex, 1, game_phase) * weight_positions * (ex % 8)

    # Declaração da variavel que representa a pontuação obtida pelas peças pretas
    score_b = 0
    # Declaração da variavel que representa a quantos movimentos foram feitos pelas peças pretas
    score_b_positions = 0
    for i, p in enumerate(b):
        # Procura se o tabuleiro a analisar contêm essa peça
        ex = board.find(p)
        # Caso contenha
        if ex >= 0:
            # Aumenta a pontuação tendo em conta a valoração da peça dada na lista 'pts.'
            score_b += pts[i]
            # Aumenta a pontuação da posição dentro em conta o peso e a posição dela (eixo) dos x (do lado dos pretos)
            score_b_positions += position(p, ex, 0, game_phase) * weight_positions * (7 - ex % 8)

    # Devolve a pontuação final como a diferença (tanto do número de peças como movimentos feitos)
    # entre as brancas e as pretas multiplicando por a variavel 'play' para determinar se é boa para nós ou má para nós
    return (score_w + score_w_positions - score_b - score_b_positions) * pow(-1, play)


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
        return (1 + ret)
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


def sucessor_states(state, player):
    ret = []

    # print('Player=%d' % player)

    for x in range(ord('a') - player * 32, ord('p') - player * 32 + 1):

        p = state.find(chr(x))
        if p < 0:
            continue
        p2 = pos1_to_pos2(p)

        pos_available = get_available_positions(state, p2, chr(x))
        # print('%c - Tot %d' % (chr(x), len(pos_available)))

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
    # print(cur_blank)
    # print(prev_not_blank)
    moved = list(set(cur_blank) & set(prev_not_blank))
    # print(moved)
    moved = moved[0]

    desc_piece = get_description_piece(prev[moved])

    fr = pos1_to_pos2(moved)
    to = pos1_to_pos2(cur.find(prev[moved]))
    # print(fr)
    # print(to)

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
        # If the state has a very bad heuristic, do not insert it in the tree
        if f_obj(s, play) < -1000:
            continue
        # Else, insert it in the tree
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


# Function mini-max with alpha-beta pruning and Null Move Pruning.
# it receives the tree, the depth, the player, the alpha, the beta and the null move
# And returns the best node and the value of the node
def minimax_alpha_beta_null_move(tr, d, play, max_player, alpha, beta, null_move):
    if d == 0 or len(tr[-1]) == 0:
        return tr, f_obj(tr[0], play)

    ret = math.inf * pow(-1, max_player)
    ret_nd = tr
    for s in tr[-1]:
        if null_move:
            aux, val = minimax_alpha_beta_null_move(s, d - 1, play, not max_player, -beta, -beta + 1, False)
            val = -val
        else:
            aux, val = minimax_alpha_beta_null_move(s, d - 1, play, not max_player, alpha, beta, True)
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

    # show_tree(states, play, nick, 0)
    print('Total nodes in the tree: %d' % count_nodes(states))

    choice, value = minimax_alpha_beta(states, depth_analysis, play, True, -math.inf, math.inf)

    # print('Choose f()=%f' % value)
    # print('State_%s_' % choice[0])

    next_move = get_next_move(states, choice)

    # print('Next_%s_' % next_move[0])
    # input('Trash')

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
