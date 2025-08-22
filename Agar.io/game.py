import random
import time

import pygame
import math
import ast
import socket

IP_serwer = '26.123.126.212'

kliet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kliet_socket.connect((IP_serwer, 55555))
kliet_socket.setblocking(True)
my_name = 'illa'

pygame.init()

screen_y = 1000
screen_x = 1000
screen = pygame.display.set_mode((screen_x, screen_y))

class My_Player():
    def __init__(self, x, y, radius, color=(0, 255, 0)):
        self.color = color
        self.radius = radius
        self.y = y
        self.x = x

    def collide(self, x, y):
        distans = math.hypot(self.x - x, self.y - y)
        return (distans < self.radius)


    def draw(self):
        pygame.draw.circle(screen, self.color, (0+screen_x//2, 0+screen_y//2), self.radius)


class Enemy_Player():
    def __init__(self, x, y, radius, color=(255,0,0)):
        self.color = color
        self.radius = radius
        self.y = y
        self.x = x

    def draw(self, x_pad, y_pad):
        pygame.draw.circle(screen, self.color, (self.x-x_pad+screen_x//2, self.y-y_pad+screen_y//2), self.radius)



eats = []
for i in range(50):
    eats.append((random.randint(-1000, 1000), random.randint(-1000, 1000), 10))

my_Player = My_Player(0, 0, 20)
eats.append((my_Player.x, my_Player.y, my_Player.radius))

kliet_socket.send(str([my_Player.x, my_Player.y, my_Player.radius, my_name]).encode())
time.sleep(0.5)

clock = pygame.time.Clock()
ran = True
while ran:
    kliet_socket.send(str([my_Player.x, my_Player.y, my_Player.radius, my_name]).encode())


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ran = False

    screen.fill((50,50,50))
    for x in range(-1000, 1000, 100):
        pygame.draw.line(screen, (100,100,100), (x-my_Player.x+screen_x//2, 1000-my_Player.y+screen_y//2), (x-my_Player.x+screen_x//2, -1000-my_Player.y+screen_y//2), 2)

    for y in range(-1000, 1000, 100):
        pygame.draw.line(screen, (100,100,100), (1000-my_Player.x+screen_x//2, y-my_Player.y+screen_y//2), (-1000-my_Player.x+screen_x//2, y-my_Player.y+screen_y//2), 2)

    pygame.draw.rect(screen, (200,200,200), pygame.Rect(-1000-my_Player.x+screen_x//2, -1000-my_Player.y+screen_y//2, 2000, 2000), 5)

    my_Player.draw()
    screen.blit(pygame.font.Font(None, 50).render(f'{int(my_Player.x)} : {int(my_Player.y)}', 1, (200,200,200)), (0, 0))

    try:
        msg = kliet_socket.recv(2048).decode()
        print(msg)
        msg=msg.split('&')[-2]
        print(msg)
        players = ast.literal_eval(msg)
        print(1)
        print('raddr=' + str(kliet_socket.getsockname()))
        if not ('raddr=' + str(kliet_socket.getsockname())) in players.keys(): ran = False
        else:
            my = players[('raddr=' + str(kliet_socket.getsockname()))]
            my_Player = My_Player(my[0], my[1], my[2])
            del players[('raddr=' + str(kliet_socket.getsockname()))]
        print(2)
        for player in players.values():
            Enemy_Player(player[0], player[1], player[2]).draw(my_Player.x, my_Player.y)
    except: print('e')

    for eat0 in eats:
        eat = Enemy_Player(eat0[0], eat0[1], eat0[2])
        eat.draw(my_Player.x, my_Player.y)
        if my_Player.collide(eat.x, eat.y):
            my_Player.radius = ((3.14 * (my_Player.radius**2) + 3.14 * (eat.radius ** 2)) / 3.14) ** 0.5
            print(my_Player.radius)
            eats.remove(eat0)
            eats.append((random.randint(-1000, 1000), random.randint(-1000, 1000), 10))




    mouse_x, mouse_y = pygame.mouse.get_pos()
    my_Player.x += min(200, max(-200, mouse_x - screen_x//2))/200
    my_Player.y += min(200, max(-200, mouse_y - screen_y//2))/200

    if my_Player.x+my_Player.radius > 1000: my_Player.x = 999-my_Player.radius
    if my_Player.x-my_Player.radius < -1000: my_Player.x = -999+my_Player.radius
    if my_Player.y+my_Player.radius > 1000: my_Player.y = 999-my_Player.radius
    if my_Player.y-my_Player.radius < -1000: my_Player.y = -999+my_Player.radius


    pygame.display.flip()

    clock.tick(120)
