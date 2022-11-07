Objetivo principal

Neste trabalho prático tem como finalidade entender a representação do estado do jogo, pesquisa em árvore, algoritmos de busca e o desenvolvimento a melhor heurística para ajudar a determinar qual a melhor jogada a fazer.
Para atingir o desenvolvimento da heurística é importante considerar que, devido à quantidade imensa de jogadas possíveis no xadrez, vamos apenas fazer uma pesquisa de profundidade 4 (Por determinar) a cada decisão de jogada feita, ou seja,
vamos apenas prever para as 4 jogadas seguintes que irão ser feitas no jogo (incluindo as do adversário) e determinar aquela onde o nosso jogador tem a melhor pontuação possível (maximizador) e o seu adversário tem a pior pontuação possível (minimizador), isto é possível usando o algoritmo "mini-max".
Mesmo fazendo a pesquisa de apenas 4 de profundidade, continuam a ser avaliados milhares de casos onde já existe uma melhor jogada possível, para evitar isto vamos usar o algoritmo "alpha-beta prunning" e permitir que as avaliações futuras na heurística sejam de maior complexidade sem comprometer o desempenho do programa.

#1 Abordagem

Inicialmente, foi usado como inspiração o código fornecido na página da cadeira denominado "client_a_bit_smart.py". Nele continha parte das funções para auxiliar o desenvolvimento deste trabalho e permitir um foco maior na função objetivo, sendo ela a maior diferenciação na complexidade dos trabalhos.
A função objetivo recebe o estado atual, recebe o estado atual e o qual jogador é que esta a ser jogado com (1 para as brancas, 0 para as pretas) e devolve uma pontuação que irá ser atribuída para esse estado. A função contida no código seguinte tinha a seguinte ordem de ideias:

— Dar peso às jogadas para avisar que as peças se mantenham na defensiva durante muitas jogadas

— Declaração das peças brancas e pretas em modo ‘string’ (a, h = torres; b, g = cavalos; c, f =bispo; d= rainha; e = rei; restantes = peões)

— Declaração da valoração de cada uma das peças comidas (10 = torres; 7 = cavalos; 6 = bispos; 100 = rainha; 9999 = rei; 1 = peões)

— Percorrer todas as peças contidas na 'string'

— Procura se o tabuleiro a analisar contêm essa peça

- Caso contenha, aumenta a pontuação tendo em conta a valoração da peça dada na lista 'pts.'

— Aumentar ou diminuir a pontuação da posição dentro em conta o peso e a posição dela (eixo) dos x (do lado dos brancos)

— Repetir o mesmo processo para as peças pretas

— Devolver a diferença entre as duas pontuações e devolver um valor positivo ou negativo dependendo da peça com que jogamos.


#2 Abordagem

Nesta abordagem, adaptaremos o código já feito e teremos em conta uma avaliação de posições, além da preservação das nossas peças.  Aqui será dado uma estrutura para cada peça representado numa lista com 64 valores (um para cada quadrado no tabuleiro), e a sua posição no tabuleiro terá uma valoração associada ao mesmo, determinando assim a jogada ideal para aquela peça através de padrões de jogo.
Também será tomado que as estruturas irão mudar dependendo do estado atual do jogo (aberturas, meio-do-jogo, fim-de-jogo) priorizando situações diferentes em cada um dos estados, onde num vai ser priorizado manter uma estrutura entre os peões e noutro será mais focado na preservação do rei e possíveis fugas.



    # Declaração da variavel que representa o número de peças existentes no tabuleiro (entre )
    num_pieces_pawn = pts[8] * board.count('i') + pts[8] * board.count('I') + pts[8] * board.count('j') + pts[
        8] * board.count('J') + pts[8] * board.count('k') + pts[8] * board.count('K') + pts[8] * board.count('l') + pts[
                          8] * board.count('L') + pts[8] * board.count('m') + pts[8] * board.count('M') + pts[
                          8] * board.count('n') + pts[8] * board.count('N') + pts[8] * board.count('o') + pts[
                          8] * board.count('O') + pts[8] * board.count('p') + pts[8] * board.count('P')
    num_pieces_rook = pts[0] * board.count('a') + pts[0] * board.count('A') + pts[0] * board.count('h') + pts[
        0] * board.count('H')
    num_pieces_knight = pts[1] * board.count('b') + pts[1] * board.count('B') + pts[1] * board.count('g') + pts[
        1] * board.count('G')
    num_pieces_bishop = pts[2] * board.count('c') + pts[2] * board.count('C') + pts[2] * board.count('f') + pts[
        2] * board.count('F')
    num_pieces_queen = pts[3] * board.count('d') + pts[3] * board.count('D')
    num_pieces_king = pts[4] * board.count('e') + pts[4] * board.count('E')

    num_pieces = num_pieces_pawn + num_pieces_rook + num_pieces_knight + num_pieces_bishop + num_pieces_queen + num_pieces_king