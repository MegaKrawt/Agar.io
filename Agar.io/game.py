import login
my_name = login.username_end
my_img_name = login.my_img_n_end

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


pygame.init()

screen_y = 100
screen_x = 100
screen = pygame.Surface((screen_x, screen_y))
screen2 = pygame.display.set_mode((900, 900))
class My_Player():
    def __init__(self, x, y, radius, color=(0, 255, 0)):
        self.color = color
        self.radius = radius
        self.y = y
        self.x = x
        self.text = font1.render(str(my_name), 1, (0,0,0))


    def collide(self, x, y):
        distans = math.hypot(self.x - x, self.y - y)
        return (distans < self.radius)


    def draw(self):
        pygame.draw.circle(screen, self.color, (0+screen_x//2, 0+screen_y//2), self.radius)
        screen.blit(pygame.transform.scale(pygame.image.load(f'awatars/{my_img_name}.png'), (self.radius*2, self.radius*2)), (screen_x//2-self.radius, screen_y//2-self.radius))
        screen.blit(self.text, (0+screen_x//2, 0+screen_y//2))


font1=pygame.font.Font(None, 40)
class Enemy_Player():
    def __init__(self, x, y, radius, name='', img_name=2, color=(255,0,0)):
        self.img_name = img_name
        self.name = name
        self.color = color
        self.radius = radius
        self.y = y
        self.x = x
        self.text = font1.render(str(self.name), 1, (0,0,0))

    def draw(self, x_pad, y_pad):
        pygame.draw.circle(screen, self.color, (self.x-x_pad+screen_x//2, self.y-y_pad+screen_y//2), self.radius)
        screen.blit(pygame.transform.scale(pygame.image.load(f'awatars/{self.img_name}.png'), (self.radius*2, self.radius*2)), (self.x-x_pad+screen_x//2-self.radius, self.y-y_pad+screen_y//2-self.radius))
        screen.blit(self.text, (self.x-x_pad+screen_x//2, self.y-y_pad+screen_y//2))



eats = []
for i in range(50):
    eats.append((random.randint(-1000, 1000), random.randint(-1000, 1000), 10))

my_Player = My_Player(0, 0, 20)
eats.append((my_Player.x, my_Player.y, my_Player.radius))

kliet_socket.send(str([my_Player.x, my_Player.y, my_Player.radius, my_name]).encode())
kliet_socket.send(str([my_Player.x, my_Player.y, my_Player.radius, my_name]).encode())
kliet_socket.send(str([my_Player.x, my_Player.y, my_Player.radius, my_name]).encode())
time.sleep(1)

clock = pygame.time.Clock()
ran = True
while ran:
    screen = pygame.Surface(((my_Player.radius*10+300), (my_Player.radius*10+300)))
    screen_x, screen_y = screen.get_size()
    kliet_socket.send(str([my_Player.x, my_Player.y, my_Player.radius, my_name, my_img_name]).encode())


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
        # print(msg)
        msg=msg.split('&')[-2]
        # print(msg)
        players = ast.literal_eval(msg)
        # print(players)
        # print(1)
        # print('raddr=' + str(kliet_socket.getsockname()))
        if not ('raddr=' + str(kliet_socket.getsockname())) in players.keys(): ran = False
        else:
            my = players[('raddr=' + str(kliet_socket.getsockname()))]
            if my[2] >= my_Player.radius:
                my_Player = My_Player(my[0], my[1], my[2])
            del players[('raddr=' + str(kliet_socket.getsockname()))]
        # print(2)
        for player in players.values():
            # print(player)
            Enemy_Player(player[0], player[1], player[2], player[3], player[4]).draw(my_Player.x, my_Player.y)
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
    try:
        my_Player.x += min(200, max(-200, mouse_x - screen2.get_width()//2))/200*120/clock.get_fps()/(min(5, my_Player.radius*0.02))
        my_Player.y += min(200, max(-200, mouse_y - screen2.get_height()//2))/200*120/clock.get_fps()/(min(5, my_Player.radius*0.02))
    except: pass
    if my_Player.x+my_Player.radius > 1000: my_Player.x = 999-my_Player.radius
    if my_Player.x-my_Player.radius < -1000: my_Player.x = -999+my_Player.radius
    if my_Player.y+my_Player.radius > 1000: my_Player.y = 999-my_Player.radius
    if my_Player.y-my_Player.radius < -1000: my_Player.y = -999+my_Player.radius

    screen.blit(pygame.font.Font(None, 50).render(f'FPS: {clock.get_fps()}', 1, (200,200,200)), (0, 100))

    scaled_virtual_screen = pygame.transform.scale(screen, (900, 900))
    screen2.blit(scaled_virtual_screen, (0,0))
    pygame.display.flip()

    clock.tick(120)

kliet_socket.close()