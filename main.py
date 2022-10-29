import math
import random
import socket
import sys

interactive_flag = False

depth_analysis = 3


def pos2_to_pos1(x2):
    return x2[0] * 8 + x2[1]


def pos1_to_pos2(x):
    row = x // 8
    col = x % 8
    return [row, col]


# Função objetivo, recebe o estado atual e o qual jogador é que esta a ser jogado com
# (1 para as brancas 0 para as pretas)
def f_obj(board, play):
    # Dá peso às jogadas para avisar que as peças se mantenham na defensiva durante muitas jogadas
    weight_positions = 1e-1
    # Declaração das peças brancas e pretas em modo ‘string’
    # a, h = torres; b,g = cavalos; c,f =bispo; d= rainha; e = rei; restantes = peões
    w = 'abcdedghijklmnop'
    b = 'ABCDEFGHIJKLMNOP'
    # Declaração da valoração de cada uma das peças comidas
    pts = [10, 7, 6, 100, 9999, 6, 7, 10, 1, 1, 1, 1, 1, 1, 1, 1]
    # Declaração da variavel que representa a pontuação obtida pelas peças brancas
    score_w = 0
    # Declaração da variavel que representa a quantos movimentos foram feitos pelas peças brancas
    score_w_positions = 0

    for i, p in enumerate(w):
        # Procura se o tabuleiro a analisar contêm essa peça
        ex = board.find(p)
        # Caso contenha
        if ex >= 0:
            # Aumenta a pontuação tendo em conta a valoração da peça dada na lista 'pts.'
            score_w += pts[i]
            # Declaração de uma variavel que transforma a posição em 1D para 2D (x, y) no tabuleiro
            p2 = pos1_to_pos2(ex)
            # Aumenta a pontuação da posição dentro em conta o peso e a posição dela (eixo) dos x (do lado dos brancos)
            score_w_positions += weight_positions * p2[0]

            # É pretendido aqui avaliar a posição das peças no tabuleiro, para isso é feito uma análise usando uma
            # "Piece-Square Table"

            # Caso a peça seja um peão
            if p == 'i' or p == 'j' or p == 'k' or p == 'l' or p == 'm' or p == 'n' or p == 'o' or p == 'p':
                # Caso estejam na linha 6
                if p2[0] == 6:
                    # Aumenta a pontuação
                    score_w += 50
                # Caso estejam na linha 5, os peões centrais aumentam 30 pontos, os laterais 20 e os extremos 10
                elif p2[0] == 5:
                    if p2[1] == 0 or p2[1] == 7 or p2[1] == 1 or p2[1] == 6:
                        score_w += 10
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w += 20
                    else:
                        score_w += 30
                # Caso estejam na linha 4, os peões centrais aumentam 25 pontos, os laterais 10 e os extremos 5
                elif p2[0] == 4:
                    if p2[1] == 0 or p2[1] == 7 or p2[1] == 1 or p2[1] == 6:
                        score_w += 5
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w += 10
                    else:
                        score_w += 25
                # Caso estejam na linha 3, os peões centrais aumentam 20 pontos, os restantes 0
                elif p2[0] == 3:
                    if p2[1] == 3 or p2[1] == 4:
                        score_w += 20
                # Caso estejam na linha 2, os peões centrais aumentam 0 pontos, os laterais -10 e os extremos 5
                elif p2[0] == 2:
                    if p2[1] == 0 or p2[1] == 7:
                        score_w += 5
                    elif p2[1] == 1 or p2[1] == 6 or p2[1] == 2 or p2[1] == 5:
                        score_w -= 10
                # Caso estejam na linha 1, os peões centrais diminuem 20 pontos, os laterais aumentam 10 e os extremos 5
                elif p2[0] == 1:
                    if p2[1] == 0 or p2[1] == 7:
                        score_w += 5
                    elif p2[1] == 1 or p2[1] == 6 or p2[1] == 2 or p2[1] == 5:
                        score_w += 10
                    else:
                        score_w -= 20

            # Caso seja um cavalo
            elif p == 'b' or p == 'g':
                # Caso esteja no extremo do tabuleiro
                if p2[0] == 0 or p2[0] == 7 or p2[1] == 0 or p2[1] == 7:
                    # Se for no canto ao centro diminui 30 pontos se for num nos 4 cantos diminui 50 pontos
                    if p2[0] == 0 and p2[1] == 0 or p2[0] == 0 and p2[1] == 7 or p2[0] == 7 and p2[1] == 0 or p2[
                        0] == 7 and p2[1] == 7:
                        score_w -= 50
                    else:
                        score_w -= 30
                # Caso esteja na linha 6
                elif p2[0] == 6:
                    # Decrementa a pontuação em 40 nos extremos e em 20 nos laterais e em 0 no centro
                    if p2[1] == 3 or p2[1] == 4:
                        score_w -= 0
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w -= 20
                    else:
                        score_w -= 40
                # Caso esteja na linha 5
                elif p2[0] == 5:
                    # Decrementa a pontuação em 30 nos extremos e em 10 nos laterais e em 0 no centro
                    if p2[1] == 3 or p2[1] == 4:
                        score_w -= 0
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w -= 10
                    else:
                        score_w -= 30
                # Caso esteja na linha 4
                elif p2[0] == 4:
                    # Incrementa a pontuação em 15 nas laterais e em 20 no centro
                    if p2[1] == 2 or p2[1] == 3 or p2[1] == 4 or p2[1] == 5:
                        score_w += 20
                    elif p2[1] == 1 or p2[1] == 6:
                        score_w += 15
                # Caso esteja na linha 3
                elif p2[0] == 3:
                    # Incrementa a pontuação em 15 nas laterais e em 20 no centro
                    if p2[1] == 2 or p2[1] == 3 or p2[1] == 4 or p2[1] == 5:
                        score_w += 20
                    elif p2[1] == 1 or p2[1] == 6:
                        score_w += 15
                # Caso esteja na linha 2
                elif p2[0] == 2:
                    # Incrementa de 5 pontos de 1-6, 10 pontos de 2-5 e 15 pontos de 3-4
                    if p2[1] == 1 or p2[1] == 6:
                        score_w += 5
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w += 10
                    elif p2[1] == 3 or p2[1] == 4:
                        score_w += 15
                # Caso esteja na linha 1
                elif p2[0] == 1:
                    # Decrementa de -20 pontos de 1-6, 0 pontos de 2-5 e 5 pontos de 3-4
                    if p2[1] == 1 or p2[1] == 6:
                        score_w -= 20
                    elif p2[1] == 3 or p2[1] == 4:
                        score_w += 5

            # Caso seja um bispo
            elif p == 'c' or p == 'f':
                # Caso esteja no extremo do tabuleiro
                if p2[0] == 0 or p2[0] == 7 or p2[1] == 0 or p2[1] == 7:
                    # Se for no canto ao centro diminui 10 pontos se for num nos 4 cantos diminui 20 pontos
                    if p2[0] == 0 and p2[1] == 0 or p2[0] == 0 and p2[1] == 7 or p2[0] == 7 and p2[1] == 0 or p2[
                        0] == 7 and p2[1] == 7:
                        score_w -= 20
                    else:
                        score_w -= 10
                # Caso esteja na linha 5
                elif p2[0] == 5:
                    # Incremente a pontuação em 5 pontos de 2 – 5 e 10 pontos de 3 – 4
                    if p2[1] == 2 or p2[1] == 5:
                        score_w += 5
                    elif p2[1] == 3 or p2[1] == 4:
                        score_w += 10
                # Caso esteja na linha 4
                elif p2[0] == 4:
                    # Incrementa a pontuação em 5 pontos de 2 – 5 e 10 pontos de 3 – 4
                    if p2[1] == 1 or p2[1] == 2 or p2[1] == 5 or p2[1] == 6:
                        score_w += 5
                    elif p2[1] == 3 or p2[1] == 4:
                        score_w += 10
                # Caso esteja na linha 3
                elif p2[0] == 3:
                    # Incrementa a pontuação em 10 pontos de 2 – 5
                    if p2[1] == 2 or p2[1] == 5 or p2[1] == 3 or p2[1] == 4:
                        score_w += 10
                # Caso esteja na linha 2
                elif p2[0] == 2:
                    # Incrementa a pontuação em 5 pontos de 1 – 6
                    if p2[1] == 1 or p2[1] == 6:
                        score_w += 5

            # Caso seja uma torre
            elif p == 'a' or p == 'h':
                # Caso esteja nos extremos do tabuleiro nas linhas 1,2,3,4 e 5
                if p2[0] == 1 or p2[0] == 2 or p2[0] == 3 or p2[0] == 4 or p2[0] == 5:
                    if p2[1] == 0 or p2[1] == 7:
                        # Decrementa a pontuação em 5 pontos
                        score_w -= 5
                # Caso esteja na linha 6
                elif p2[0] == 6:
                    # Caso esteja nos cantos incrementa 5 pontos senão incrementa 10 pontos
                    if p2[1] == 0 or p2[1] == 7:
                        score_w += 5
                    else:
                        score_w += 10
                # Caso esteja na linha 0
                elif p2[0] == 0:
                    # Caso esteja no centro, incrementa 5 pontos
                    if p2[1] == 3 or p2[1] == 4:
                        score_w += 5

            # Caso seja uma rainha
            elif p == 'd':
                # Caso esteja nos cantos do tabuleiro
                if p2[0] == 0 and p2[1] == 0 or p2[0] == 0 and p2[1] == 7 or p2[0] == 7 and p2[1] == 0 or p2[0] == 7 and \
                        p2[1] == 7:
                    # Decrementa a pontuação em 20 pontos
                    score_w -= 10
                # Caso esteja nas bordas do tabuleiro decrementa 10 pontos
                elif p2[0] == 0 or p2[0] == 7 or p2[1] == 0 or p2[1] == 7:
                    score_w -= 10
                # Caso esteja entre as linhas 1 e 6 e entre as colunas 2 e 5, incrementa 5 pontos
                elif 0 < p2[0] < 7 and 1 < p2[1] < 6:
                    score_w += 5

            # Caso seja um rei (POR FAZER)

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
            # Declaração de uma variavel que transforma a posição em 1D para 2D (x, y) no tabuleiro
            p2 = pos1_to_pos2(ex)
            # Aumenta a pontuação da posição dentro em conta o peso e a posição dela (eixo) dos x (do lado dos pretos)
            score_b_positions += weight_positions * (7 - p2[0])

            # Caso seja um peão
            if p == 'I' or p == 'J' or p == 'K' or p == 'L' or p == 'M' or p == 'N' or p == 'O' or p == 'P':
                # Caso esteja na linha 1
                if p2[0] == 1:
                    # Aumenta a pontuação
                    score_w += 50
                # Caso esteja na linha 2, os peões centrais aumentam 30 pontos, os laterais 20 e os extremos 10
                elif p2[0] == 2:
                    if p2[1] == 3 or p2[1] == 4:
                        score_w += 30
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w += 20
                    else:
                        score_w += 10
                # Caso esteja na linha 3, os peões centrais aumentam 25 pontos, os laterais 10 e os extremos 5
                elif p2[0] == 3:
                    if p2[1] == 3 or p2[1] == 4:
                        score_w += 25
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w += 10
                    else:
                        score_w += 5
                # Caso esteja na linha 4, os peões centrais aumentam 20 pontos, os restantes 0
                elif p2[0] == 4:
                    if p2[1] == 3 or p2[1] == 4:
                        score_w += 20
                # Caso esteja na linha 5, os peões centrais aumentam 0 pontos, os laterais -10 e os extremos 5
                elif p2[0] == 5:
                    if p2[1] == 3 or p2[1] == 4:
                        score_w += 0
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w -= 10
                    else:
                        score_w -= 5
                # Caso esteja na linha 6, os peões centrais diminuem 20 pontos, os laterais aumentam 10 e os extremos 5
                elif p2[0] == 6:
                    if p2[1] == 3 or p2[1] == 4:
                        score_w -= 20
                    elif p2[1] == 2 or p2[1] == 5:
                        score_w += 10
                    else:
                        score_w += 5

            # Caso seja um cavalo
            elif p == 'B' or p == 'G':
                # Caso esteja no extremo do tabuleiro
                if p2[0] == 0 or p2[0] == 7 or p2[1] == 0 or p2[1] == 7:
                    # Se for no canto ao centro diminui 30 pontos se for num nos 4 cantos diminui 50 pontos
                    if p2[0] == 0 and p2[1] == 0 or p2[0] == 0 and p2[1] == 7 or p2[0] == 7 and p2[1] == 0 or p2[
                        0] == 7 and p2[1] == 7:
                        score_b -= 50
                    else:
                        score_b -= 30
                # Caso esteja na linha 1
                elif p2[0] == 1:
                    # Decrementa a pontuação em 40 nos extremos e em 20 nos laterais e em 0 no centro
                    if p2[1] == 3 or p2[1] == 4:
                        score_b -= 0
                    elif p2[1] == 2 or p2[1] == 5:
                        score_b -= 20
                    else:
                        score_b -= 40
                # Caso esteja na linha 2
                elif p2[0] == 2:
                    # Decrementa a pontuação em 30 nos extremos e em 10 nos laterais e em 0 no centro
                    if p2[1] == 3 or p2[1] == 4:
                        score_b -= 0
                    elif p2[1] == 2 or p2[1] == 5:
                        score_b -= 10
                    else:
                        score_b -= 30
                # Caso esteja na linha 3
                elif p2[0] == 3:
                    # Incrementa a pontuação em 15 nas laterais e em 20 no centro
                    if p2[1] == 3 or p2[1] == 4:
                        score_b += 20
                    elif p2[1] == 2 or p2[1] == 5:
                        score_b += 15
                # Caso esteja na linha 4
                elif p2[0] == 4:
                    # Incrementa a pontuação em 15 nas laterais e em 20 no centro
                    if p2[1] == 3 or p2[1] == 4:
                        score_b += 20
                    elif p2[1] == 2 or p2[1] == 5:
                        score_b += 15
                # Caso esteja na linha 5
                elif p2[0] == 5:
                    # Incrementa de 5 pontos de 1-6, 10 pontos de 2-5 e 15 pontos de 3-4
                    if p2[1] == 3 or p2[1] == 4:
                        score_b += 15
                    elif p2[1] == 2 or p2[1] == 5:
                        score_b += 10
                    elif p2[1] == 1 or p2[1] == 6:
                        score_b += 5
                # Caso esteja na linha 6
                elif p2[0] == 6:
                    # Decrementa de -20 pontos de 1-6, 0 pontos de 2-5 e 5 pontos de 3-4
                    if p2[1] == 3 or p2[1] == 4:
                        score_b -= 20
                    elif p2[1] == 1 or p2[1] == 6:
                        score_b += 5

            # Caso seja um bispo
            elif p == 'C' or p == 'F':
                # Caso esteja no extremo do tabuleiro
                if p2[0] == 0 or p2[0] == 7 or p2[1] == 0 or p2[1] == 7:
                    # Se for no canto ao centro diminui 10 pontos se for num nos 4 cantos diminui 20 pontos
                    if p2[0] == 0 and p2[1] == 0 or p2[0] == 0 and p2[1] == 7 or p2[0] == 7 and p2[1] == 0 or p2[
                        0] == 7 and p2[1] == 7:
                        score_w -= 20
                    else:
                        score_w -= 10
                # Caso esteja na linha 2
                elif p2[0] == 2:
                    # Incremente a pontuação em 5 pontos de 2 – 5 e 10 pontos de 3 – 4
                    if p2[1] == 2 or p2[1] == 5:
                        score_w += 5
                    elif p2[1] == 3 or p2[1] == 4:
                        score_w += 10
                # Caso esteja na linha 3
                elif p2[0] == 3:
                    # Incrementa a pontuação em 5 pontos de 2 – 5 e 10 pontos de 3 – 4
                    if p2[1] == 1 or p2[1] == 2 or p2[1] == 5 or p2[1] == 6:
                        score_w += 5
                    elif p2[1] == 3 or p2[1] == 4:
                        score_w += 10
                # Caso esteja na linha 4
                elif p2[0] == 4:
                    # Incrementa a pontuação em 10 pontos de 2 – 5
                    if p2[1] == 2 or p2[1] == 5 or p2[1] == 3 or p2[1] == 4:
                        score_w += 10
                # Caso esteja na linha 5
                elif p2[0] == 5:
                    # Incrementa a pontuação em 5 pontos de 1 – 6
                    if p2[1] == 1 or p2[1] == 6:
                        score_w += 5

            # Caso seja uma torre
            elif p == 'A' or p == 'H':
                # Caso esteja nos extremos do tabuleiro nas linhas 1,2,3,4 e 5
                if p2[0] == 1 or p2[0] == 2 or p2[0] == 3 or p2[0] == 4 or p2[0] == 5:
                    if p2[1] == 0 or p2[1] == 7:
                        # Decrementa a pontuação em 5 pontos
                        score_w -= 5
                # Caso esteja na linha 1
                elif p2[0] == 1:
                    # Caso esteja nos cantos incrementa 5 pontos senão incrementa 10 pontos
                    if p2[1] == 0 or p2[1] == 7:
                        score_w += 5
                    else:
                        score_w += 10
                # Caso esteja na linha 7
                elif p2[0] == 7:
                    # Caso esteja no centro, incrementa 5 pontos
                    if p2[1] == 3 or p2[1] == 4:
                        score_w += 5

            # Caso seja uma rainha
            elif p == 'D':
                # Caso esteja nos cantos do tabuleiro
                if p2[0] == 0 and p2[1] == 0 or p2[0] == 0 and p2[1] == 7 or p2[0] == 7 and p2[1] == 0 or p2[0] == 7 and \
                        p2[1] == 7:
                    # Decrementa a pontuação em 20 pontos
                    score_w -= 10
                # Caso esteja nas bordas do tabuleiro decrementa 10 pontos
                elif p2[0] == 0 or p2[0] == 7 or p2[1] == 0 or p2[1] == 7:
                    score_w -= 10
                # Caso esteja entre as linhas 1 e 6 e entre as colunas 2 e 5, incrementa 5 pontos
                elif 0 < p2[0] < 7 and 1 < p2[1] < 6:
                    score_w += 5

            # Caso seja um rei (POR FAZER)

    # Devolve a pontuação final como a diferença (tanto do número de peças como movimentos feitos)
    # entre as brancas e as pretas multiplicando por a variavel 'play' para determinar se é boa para nós ou má para nós
    return (score_w + score_w_positions - score_b - score_b_positions) * pow(-1, play)


# OPENINGS — Aberturas
# Priorizar movimentos onde o cavalo está no centro do tabuleiro
# Priorizar movimentos onde o cavalo não fica nas bordas do tabuleiro
# Priorizar movimentos onde os peões do centro são preservados
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
            if d[0] == 'PN':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                continue
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
