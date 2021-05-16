import arcade
import PySimpleGUI as sg
import numpy
import pygame
import queue as q
import copy
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (101, 67, 33)
BLUE = (18, 0, 179)
YELLOW = (255, 231, 0)
PINK = (239, 0, 135)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 15
HEIGHT = 15
WINDOW_SIZE = [715, 715]
MARGIN = 2


# Set title of screen


class pos_atual():

    def __init__(self, x, y, custo, custo_a_star):
        self.x = x  # Posicao x
        self.y = y  # Posicao y
        self.caminho_perc = []  # Armazena os caminhos percorridos
        self.custo = custo  # Custo para o busca cega
        self.custo_star = custo_a_star  # Custo real sem a heuristica pro a*

    def set_caminhoList(self, caminho):
        self.caminho_perc = copy.copy(caminho)

    def set_caminho(self, caminho):
        self.caminho_perc.append(caminho)

def init_screen():
    global screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Projeto IA")
    # This sets the margin between each cell
    pygame.init()
    global clock
    clock = pygame.time.Clock()

def analisa_repeticao(repetidos, posicao):
    # Verifica se ja foi aberto
    for pos_lista in repetidos:
        if pos_lista.x == posicao.x and pos_lista.y == posicao.y:
            return True
    return False


def menorCusto(e):
    return e.custo


def BuscaCegaUniforme(matrizMapa, matriz_aux, inicio, final):
    
    # Instancia um objeto, passando (posicao x inicial) (posicao y inicial) (custo busca cega) (custo a*)
    no_atual = pos_atual(inicio[0], inicio[1], 0, 0)
    no_atual.set_caminho(inicio)
    borda = []
    repetidos = []
    repetidos.append(no_atual)
    cont = 0

    borda.append(no_atual)

    # Repetir enquanto a borda não estiver vazia
    while True:
        # Retira o primeiro elemento da fila

        if cont == 0:
            no_atual = borda.pop(0)

        # Verificar se caminho atual é o final
        if no_atual.x == final[0] and no_atual.y == final[1]:
            # Exibir caminho na tela, printar caminho andando e custo total
            # no_atual.caminho_perc e no_atual.custo PRINTAR GRÁFICO
            print('\nCusto total:', no_atual.custo)
            print('Caminho percorrido:', no_atual.caminho_perc)
            print('Caminhos abertos:', cont)
            
            # Printar caminho final na tela
            lista_caminho = []
            for i in range(len(no_atual.caminho_perc)):
                for j in range(2):
                    lista_caminho.append(no_atual.caminho_perc[i][j])

            i = 0
            while i != len(lista_caminho):
                if i == 0:  # Printar inicio
                    matriz_aux[lista_caminho[i]][lista_caminho[i + 1]] = 7
                if i == ((len(lista_caminho)) - 2):  # Printar final
                    matriz_aux[lista_caminho[i]][lista_caminho[i + 1]] = 7
                elif i != 0:  # Printar caminho entre inicio e final
                    matriz_aux[lista_caminho[i]][lista_caminho[i + 1]] = 6

                ImprimeMatrix(matriz_aux)
                i += 1
                i += 1

            espera()
            # Fechar programa
            exit(0)
            break

        # DIREITA
        if no_atual.x + 1 <= 41:
            if [no_atual.x + 1, no_atual.y] not in no_atual.caminho_perc:
                no_filho = pos_atual(no_atual.x + 1, no_atual.y,matrizMapa[no_atual.x + 1][no_atual.y] + no_atual.custo, 0)
                variavel = copy.copy(no_atual.caminho_perc)
                no_filho.set_caminhoList(variavel)
                no_filho.set_caminho([no_atual.x + 1, no_atual.y])
                borda.append(no_filho)
                matrizMapa[no_atual.x][no_atual.y] = 8

                # PRINTAR A EXPANSÃO

        # ESQUERDA
        if no_atual.x - 1 >= 0:
            if [no_atual.x - 1, no_atual.y] not in no_atual.caminho_perc:
                no_filho = pos_atual(no_atual.x - 1, no_atual.y, matrizMapa[no_atual.x - 1][no_atual.y] + no_atual.custo, 0)
                variavel = copy.copy(no_atual.caminho_perc)
                no_filho.set_caminhoList(variavel)
                no_filho.set_caminho([no_atual.x - 1, no_atual.y])
                borda.append(no_filho)
                matriz_aux[no_atual.x][no_atual.y] = 8

                # PRINTAR A EXPANSÃO

        # BAIXO
        if no_atual.y + 1 <= 41:
            if [no_atual.x, no_atual.y + 1] not in no_atual.caminho_perc:
                no_filho = pos_atual(no_atual.x, no_atual.y + 1,matrizMapa[no_atual.x][no_atual.y + 1] + no_atual.custo, 0)
                variavel = copy.copy(no_atual.caminho_perc)
                no_filho.set_caminhoList(variavel)
                no_filho.set_caminho([no_atual.x, no_atual.y + 1])
                borda.append(no_filho)
                matriz_aux[no_atual.x][no_atual.y] = 8

                # PRINTAR A EXPANSÃO

        # CIMA
        if no_atual.y - 1 >= 0:
            if [no_atual.x, no_atual.y - 1] not in no_atual.caminho_perc:
                no_filho = pos_atual(no_atual.x, no_atual.y - 1,matrizMapa[no_atual.x][no_atual.y - 1] + no_atual.custo, 0)
                variavel = copy.copy(no_atual.caminho_perc)
                no_filho.set_caminhoList(variavel)
                no_filho.set_caminho([no_atual.x, no_atual.y - 1])
                borda.append(no_filho)
                # matriz_aux[no_atual.x][no_atual.y] = 6
                matriz_aux[no_atual.x][no_atual.y] = 8

                # PRINTAR A EXPANSÃO

        borda.sort(key=menorCusto)

        while analisa_repeticao(repetidos, no_atual):
            if (borda == []):
                break
            no_atual = borda.pop(0)
            cont += 1  # Contar caminhos abertos

        ImprimeMatrix(matriz_aux)
        repetidos.append(no_atual)

    # Desenhar na tela
    ImprimeMatrix(matriz_aux)


def calculaDelta(pos_x, pos_y, final, custo):
    # Heuristica utilizado no a*
    dx = abs(final[0] - pos_x)
    dy = abs(final[1] - pos_y)
    return custo + (dx + dy)


def a_star(matrizMapa, matriz_aux, inicio, final):

    # Instancia um objeto, passando (posicao x inicial) (posicao y inicial) (custo busca cega) (custo a*)
    no_atual = pos_atual(inicio[0], inicio[1], 0, 0)
    no_atual.set_caminho(inicio)
    borda = []
    repetidos = []
    repetidos.append(no_atual)
    cont = 0

    # Colocar no nó de inicio
    borda.append(no_atual)

    # Repetir enquanto a borda não estiver vazia
    while True:
        # Retira o primeiro elemento da fila

        if cont == 0:
            no_atual = borda.pop(0)

        # Verificar se caminho atual é o final
        if no_atual.x == final[0] and no_atual.y == final[1]:
            # Exibir caminho na tela, printar caminho andando e custo total
            # no_atual.caminho_perc e no_atual.custo PRINTAR GRÁFICO
            print('\nCusto total:', no_atual.custo_star)
            print('Caminho percorrido:', no_atual.caminho_perc)
            print('Caminhos abertos:', cont)
            
            # Printar caminho final na tela
            lista_caminho = []
            for i in range(len(no_atual.caminho_perc)):
                for j in range(2):
                    lista_caminho.append(no_atual.caminho_perc[i][j])

            i = 0
            while i != len(lista_caminho):
                if i == 0:  # Printar inicio
                    matriz_aux[lista_caminho[i]][lista_caminho[i + 1]] = 7
                if i == ((len(lista_caminho)) - 2):  # Printar final
                    matriz_aux[lista_caminho[i]][lista_caminho[i + 1]] = 7
                elif i != 0:  # Printar caminho entre inicio e final
                    matriz_aux[lista_caminho[i]][lista_caminho[i + 1]] = 6

                ImprimeMatrix(matriz_aux)
                i += 1
                i += 1

            espera()
            # Fechar programa
            exit(0)
            break

        # DIREITA
        if no_atual.x + 1 <= 41:
            if [no_atual.x + 1, no_atual.y] not in no_atual.caminho_perc:
                # Calcular o custo real sem a heuristica
                custo_star = (matrizMapa[no_atual.x + 1][no_atual.y] + no_atual.custo_star)

                DELTA = calculaDelta(no_atual.x + 1, no_atual.y, final,(matrizMapa[no_atual.x + 1][no_atual.y] + no_atual.custo))
                no_filho = pos_atual(no_atual.x + 1, no_atual.y, DELTA, custo_star)
                variavel = copy.copy(no_atual.caminho_perc)
                no_filho.set_caminhoList(variavel)
                no_filho.set_caminho([no_atual.x + 1, no_atual.y])
                borda.append(no_filho)
                matriz_aux[no_atual.x][no_atual.y] = 8

        # ESQUERDA
        if no_atual.x - 1 >= 0:
            if [no_atual.x - 1, no_atual.y] not in no_atual.caminho_perc:
                # Calcular o custo real sem a heuristica
                custo_star = (matrizMapa[no_atual.x - 1][no_atual.y] + no_atual.custo_star)

                DELTA = calculaDelta(no_atual.x - 1, no_atual.y, final,(matrizMapa[no_atual.x - 1][no_atual.y] + no_atual.custo))
                no_filho = pos_atual(no_atual.x - 1, no_atual.y, DELTA, custo_star)
                variavel = copy.copy(no_atual.caminho_perc)
                no_filho.set_caminhoList(variavel)
                no_filho.set_caminho([no_atual.x - 1, no_atual.y])
                borda.append(no_filho)
                matriz_aux[no_atual.x][no_atual.y] = 8

                # PRINTAR A EXPANSÃO

        # BAIXO
        if no_atual.y + 1 <= 41:
            if [no_atual.x, no_atual.y + 1] not in no_atual.caminho_perc:
                # Calcular o custo real sem a heuristica
                custo_star = (matrizMapa[no_atual.x][no_atual.y + 1] + no_atual.custo_star)

                DELTA = calculaDelta(no_atual.x, no_atual.y + 1, final,(matrizMapa[no_atual.x][no_atual.y + 1] + no_atual.custo))
                no_filho = pos_atual(no_atual.x, no_atual.y + 1, DELTA, custo_star)
                variavel = copy.copy(no_atual.caminho_perc)
                no_filho.set_caminhoList(variavel)
                no_filho.set_caminho([no_atual.x, no_atual.y + 1])
                borda.append(no_filho)
                matriz_aux[no_atual.x][no_atual.y] = 8

                # PRINTAR A EXPANSÃO

        # CIMA
        if no_atual.y - 1 >= 0:
            if [no_atual.x, no_atual.y - 1] not in no_atual.caminho_perc:
                # Calcular o custo real sem a heuristica
                custo_star = (matrizMapa[no_atual.x][no_atual.y - 1] + no_atual.custo_star)

                DELTA = calculaDelta(no_atual.x, no_atual.y - 1, final,(matrizMapa[no_atual.x][no_atual.y - 1] + no_atual.custo))
                no_filho = pos_atual(no_atual.x, no_atual.y - 1, DELTA, custo_star)
                variavel = copy.copy(no_atual.caminho_perc)
                no_filho.set_caminhoList(variavel)
                no_filho.set_caminho([no_atual.x, no_atual.y - 1])
                borda.append(no_filho)
                matriz_aux[no_atual.x][no_atual.y] = 8

                # PRINTAR A EXPANSÃO

        borda.sort(key=menorCusto)

        while analisa_repeticao(repetidos, no_atual):
            if (borda == []):
                break
            no_atual = borda.pop(0)
            cont += 1
            # PRINTAR MATRIZ

        ImprimeMatrix(matriz_aux)
        repetidos.append(no_atual)

        # Desenhar na tela
    ImprimeMatrix(matrizMapa)

def espera():
    done = False
    while not done:
        # Set the screen background
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True
        screen.fill(BLACK)


def ImprimeMatrix(matrizMapa):
    # Draw the grid
    for row in range(42):
        for column in range(42):
            color = WHITE
            if matrizMapa[row][column] == 1:
                color = GREEN
            if matrizMapa[row][column] == 5:
                color = BROWN
            if matrizMapa[row][column] == 10:
                color = BLUE
            if matrizMapa[row][column] == 15:
                color = RED
            if matrizMapa[row][column] == 7:
                color = BLACK
            if matrizMapa[row][column] == 8:
                color = PINK
            if matrizMapa[row][column] == 6:
                color = WHITE

            pygame.draw.rect(screen, color,
                             [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

        # Limit to 60 frames per second
        clock.tick(5000)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


def main():
    matrizEntrada = []
    with open('ArquivoEntrada.txt', 'r') as f:
        # Lê a primeira e segunda linha do arquivo
        pos_incial = f.readline()
        pos_final = f.readline()
        # Lê o restante das linhas do arquivo e salva numa matriz de entrada
        for linha in f:
            linha = linha.rstrip()
            matrizEntrada.append(linha.split(','))

    # Criar a matriz
    matrizMapa = []
    matriz_aux = []
    for i in range(42):
        matrizMapa.append([0] * 42)
        matriz_aux.append([0] * 42)
    # Passar os dados lidos do arquivo para a matriz do mapa do tipo inteiro
    for i in range(42):
        for j in range(42):

            if int(matrizEntrada[i][j]) == 1:
                matrizMapa[i][j] = 1
                matriz_aux[i][j] = 1
            if int(matrizEntrada[i][j]) == 2:
                matrizMapa[i][j] = 5
                matriz_aux[i][j] = 5
            if int(matrizEntrada[i][j]) == 3:
                matrizMapa[i][j] = 10
                matriz_aux[i][j] = 10
            if int(matrizEntrada[i][j]) == 4:
                matrizMapa[i][j] = 15
                matriz_aux[i][j] = 15

    # Printar em forma de matriz
    for i in range(42):
        print(matrizMapa[i])

    # Vetores que contem as coordenadas X,Y inicial e final
    inicial = pos_incial.split(',')
    inicial[0] = int(inicial[0])
    inicial[1] = int(inicial[1])

    final = pos_final.split(',')
    final[0] = int(final[0])
    final[1] = int(final[1])

    # MENU
    # ImprimeMatrix(matrizMapa)
    # matrizMapa[4][2] = 4
    # ImprimeMatrix(matrizMapa)
    # espera()
    print('\n 1 - Busca Cega Uniforme\n 2 - A*')

    choice = input('\nDigite uma opcao: ')
    



    if choice == '1':
        
        init_screen()
        BuscaCegaUniforme(matrizMapa, matriz_aux, inicial, final)
    if choice == '2':
        
        init_screen()
        a_star(matrizMapa, matriz_aux, inicial, final)


main()