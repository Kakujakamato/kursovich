import pygame
import sys
import numpy as np
import os
import threading
import socket

HOST = '192.168.33.1'
PORT = 55555
BG_COLOR = (30, 145, 150)
BROAD_COL = 4
BROAD_ROW = BROAD_COL
LINE_color = (0, 0, 0)
game_over = False
connection_established = False
conn, addr = None, None

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)


def receive_data():
    global turn
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        x, y, = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            game_over = True
        if Broad[y][x] == 0:
            Broad[y][x] = 2
            player = 2
            scren.blit(letterO, (x*100, y*100))
            check_win(player)
            


def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = sock.accept()
    print('client is connected')
    connection_established = True
    receive_data()


create_thread(waiting_for_connection)

letterX = pygame.image.load(os.path.join('res1', 'letterx.png'))
letterO = pygame.image.load(os.path.join('res1', 'lettero.png'))
scren = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Game Sever")
scren.fill(BG_COLOR)
Broad = np.zeros((BROAD_ROW, BROAD_COL))


def check_win(player):
    for col in range(BROAD_COL):
        if Broad[0][col] == player and Broad[1][col] == player and Broad[2][col] == player and Broad[3][col] == player:
            return True
    for row in range(BROAD_ROW):
        if Broad[row][0] == player and Broad[row][1] == player and Broad[row][2] == player and Broad[row][3] == player:
            return True
    if Broad[3][0] == player and Broad[1][2] == player and Broad[2][1] == player and Broad[0][3] == player:
        return True
    if Broad[0][0] == player and Broad[1][1] == player and Broad[2][2] == player and Broad[3][3] == player:
        return True
    return False



def Draw_lines():
    pygame.draw.line(scren, LINE_color, (100, 0), (100, 400), 2)
    pygame.draw.line(scren, LINE_color, (200, 0), (200, 400), 2)
    pygame.draw.line(scren, LINE_color, (300, 0), (300, 400), 2)
    pygame.draw.line(scren, LINE_color, (0, 100), (400, 100), 2)
    pygame.draw.line(scren, LINE_color, (0, 200), (400, 200), 2)
    pygame.draw.line(scren, LINE_color, (0, 300), (400, 300), 2)


Draw_lines()


def restart():
    scren.fill( BG_COLOR )
    Draw_lines()
    for y in range(len(Broad)):
        for x in range(len(Broad[1])):
            Broad[y][x] = 0

running = True
player = 1
turn = True
playing = 'True'

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
            if check_win(2):
                game_over = True
                print('player2 win')
                playing = False
            if check_win(1):
                game_over = True
                print('player1 win')
                playing = False
            if pygame.mouse.get_pressed()[0]:
                if turn and not game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 100, pos[1] // 100
                    if Broad[cellY][cellX] == 0:
                        Broad[cellY][cellX] = player
                        scren.blit(letterX, (cellX*100, cellY*100))
                        send_data = '{}-{}-{}-{}'.format(
                        cellX, cellY, 'yourturn', playing).encode()
                        conn.send(send_data)
                        turn = False
                        if check_win(2):
                            game_over = True
                            print('player2 win')
                            playing = False
                        if check_win(1):
                            game_over = True
                            print('player1 win')
                            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                restart()
                game_over = False
                playing = 'True'
            elif event.key == pygame.K_ESCAPE:
                running = False

    pygame.display.update()
