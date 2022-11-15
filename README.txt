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

Nesta abordagem, adaptaremos o código já feito e teremos em conta uma avaliação de posições, além da preservação das nossas peças. Aqui será dado uma estrutura para cada peça representado numa lista com 64 valores (um para cada quadrado no tabuleiro), e a sua posição no tabuleiro terá uma valoração associada ao mesmo, determinando assim a jogada ideal para aquela peça através de padrões de jogo.
Também será tomado que as estruturas irão mudar a depender do estado atual do jogo (aberturas, meio-do-jogo, fim-de-jogo) priorizando situações diferentes em cada um dos estados, onde num vai ser priorizado manter uma estrutura entre os peões e noutro será mais focado na preservação do rei e possíveis fugas.


#3 Abordagem

Na seguinte abordagem, foi implementada uma função dado uma peça, irá determinar quais peças ela ameaça (seja acabada).
A função irá receber o tabuleiro e a peça a analisar e irá devolver uma lista com as peças ameaçadas em formato 'string'.

Contêm o seguinte processo de análise:
— Obtem a peça a analisar e a sua posição no tabuleiro em 2D
— Verifica qual a peça em questão e qual o jogador que a tem
— Percorre num ciclo for, todos os quadrados que essa peça pode legalmente mover-se
— Caso encontre um quadrado ocupado por uma peça adversári, adiciona essa peça à lista de peças ameaçadas
— No final retorna a lista de peças ameaçadas
— Na função objetivo, irá ser declarado a variavel que guarda as peças ameaçadas e irá verificar qual a peça em questão.
— Após determinar qual a peça em questão, irá ser dado uma valoração á variavel 'score_w_threats' ou 'score_b_threats', dependendo do jogador que a tem, relativamente á importância dessa peça no jogo.