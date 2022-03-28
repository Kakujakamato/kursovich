import pygame
import numpy as np
import os
import threading
import socket

# constant
PORT = 55555
BG_COLOR = (30, 145, 150)
BROAD_COL = 4
BROAD_ROW = BROAD_COL
POSITION_X_ON_BROAD = 100
POSITION_Y_ON_BROAD = 100
THIN_LEVER_OF_LINES = 2
START_POSITION = 0
END_POSITION = 400
COUNT_DOWN_TIME = 10
LINE_color = (0, 0, 0)
game_over = False
connection_established = False
conn, addr = None, None
player = 2
running = True
turn = False
playing = 'True'


def create_thread(target):
    thread = threading.Thread(target=target)  # control the of data form sever
    thread.daemon = True
    thread.start()


# af_client is the ipv4 for socket, TCP in socket use stream
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), PORT))  # get ip of the sever to connect


def receive_data():
    global turn, game_over
    while True:
        data = sock.recv(1024).decode()  # 1024 is the size of data limitation
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            game_over = True
        if Broad[y][x] == 0:
            Broad[y][x] = 1
            player = 1
            check_win(player)
            screen.blit(letterX, (x*100, y*100))


create_thread(receive_data)


letterX = pygame.image.load(os.path.join('Imgfile', 'letterx.png'))
letterO = pygame.image.load(os.path.join('Imgfile', 'lettero.png'))

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Game Client - Player 2")
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


def WinCondition():
    global playing,game_over
    if check_win(2):
        game_over = True
        playing = 'False'
        print('player2 win\n Press space to continute')
    if check_win(1):
        game_over = True
        playing = 'False'
        print('player1 win\n Press space to continute')
    return(game_over, playing)


def restart():
    screen.fill(BG_COLOR)
    Draw_lines()
    for y in range(len(Broad)):
        for x in range(len(Broad[1])):
            Broad[y][x] = 0  # set all squel back to 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            WinCondition()
            if pygame.mouse.get_pressed()[0]:
                if turn and (playing == 'True'):
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 100, pos[1] // 100
                    if Broad[cellY][cellX] == 0:
                        Broad[cellY][cellX] = player
                        screen.blit(letterO, (cellX*100, cellY*100))
                        send_data = '{}-{}-{}-{}'.format(
                            cellX, cellY, 'yourturn', playing).encode()
                        sock.send(send_data)
                        turn = False
            else:
                for y in range(len(Broad)):
                    for x in range(len(Broad[1])):
                        if (Broad[y][x] != 0):
                            game_over = True
                            print('Draw\n Press space to continute')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                restart()
                game_over = False
                playing = 'True'
    pygame.display.update()