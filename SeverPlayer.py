import pygame
import sys
import numpy as np
import os
import threading
import socket

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'

# Address host.
HOST = '192.168.33.1'
PORT = 55555
BG_COLOR = (30, 145, 150)
BROAD_COL = 4
BROAD_ROW = BROAD_COL
POSITION_X_ON_BROAD = 100
POSITION_Y_ON_BROAD = 100
THIN_LEVER_OF_LINES = 2
START_POSITION = 0
END_POSITION = 400
LINE_color = (0, 0, 0)
game_over = False
connection_established = False
conn, addr = None, None
running = True
player = 1
turn = True
playing = 'True'




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
            screen.blit(letterO, (x*100, y*100))
            check_win(player)


def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = sock.accept()
    print('Client is connected')
    connection_established = True
    receive_data()


create_thread(waiting_for_connection)

letterX = pygame.image.load(os.path.join('res1', 'letterx.png'))
letterO = pygame.image.load(os.path.join('res1', 'lettero.png'))
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Game Sever")
screen.fill(BG_COLOR)
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
    pygame.draw.line(screen, LINE_color, (POSITION_X_ON_BROAD, START_POSITION),
                     (POSITION_X_ON_BROAD, END_POSITION), THIN_LEVER_OF_LINES)
    pygame.draw.line(screen, LINE_color, (2*POSITION_X_ON_BROAD, START_POSITION),
                     (2*POSITION_X_ON_BROAD, END_POSITION), THIN_LEVER_OF_LINES)
    pygame.draw.line(screen, LINE_color, (3*POSITION_X_ON_BROAD, START_POSITION),
                     (3*POSITION_Y_ON_BROAD, END_POSITION), THIN_LEVER_OF_LINES)
    pygame.draw.line(screen, LINE_color, (START_POSITION, POSITION_Y_ON_BROAD),
                     (END_POSITION, POSITION_Y_ON_BROAD), THIN_LEVER_OF_LINES)
    pygame.draw.line(screen, LINE_color, (START_POSITION, 2*POSITION_Y_ON_BROAD),
                     (END_POSITION, 2*POSITION_Y_ON_BROAD), THIN_LEVER_OF_LINES)
    pygame.draw.line(screen, LINE_color, (START_POSITION, 3*POSITION_Y_ON_BROAD),
                     (END_POSITION, 3*POSITION_Y_ON_BROAD), THIN_LEVER_OF_LINES)


Draw_lines()


def restart():
    screen.fill(BG_COLOR)
    Draw_lines()
    for y in range(len(Broad)):
        for x in range(len(Broad[1])):
            Broad[y][x] = 0


def askforreplay(game_over):
    print('Press Space to continute')
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and game_over:
            game_over = False
            playing = 'True'
            restart()
        # elif event.key == pygame.K_ESCAPE:
        #     running = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
            if check_win(1):
                game_over = True
                playing = 'False'
                print('player1 win')
                askforreplay(playing, game_over, running)
            if check_win(2):
                game_over = True
                playing = 'False'
                print('player2 win')
                askforreplay(playing, game_over, running)
            if pygame.mouse.get_pressed()[0]:
                if turn and (playing == 'True'):
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 100, pos[1] // 100
                    if Broad[cellY][cellX] == 0:
                        Broad[cellY][cellX] = player
                        screen.blit(letterX, (cellX*100, cellY*100))
                        send_data = '{}-{}-{}-{}'.format(
                            cellX, cellY, 'yourturn', playing).encode()
                        conn.send(send_data)
                        turn = False
                        if check_win(1):
                            game_over = True
                            playing = 'False'
                            print('player1 win')
                            askforreplay(playing, game_over, running)
                        if check_win(2):
                            game_over = True
                            playing = 'False'
                            print('player2 win')
                            askforreplay(playing, game_over, running)

    pygame.display.update()
