import random

import pygame
import math

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



enemy_Players = []
for i in range(50):
    enemy_Players.append(Enemy_Player(random.randint(-1000, 1000), random.randint(-1000, 1000), 10))

my_Player = My_Player(0, 0, 20)


clock = pygame.time.Clock()
ran = True
while ran:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ran = False

    screen.fill((50,50,50))
    for x in range(-10, 10):
        for y in range(-10, 10):
            xx= x*100-my_Player.x+screen_x//2
            yy= y*100-my_Player.y+screen_y//2
            pygame.draw.line(screen, (100,100,100), (xx, yy), (xx, yy+100), 2)
            pygame.draw.line(screen, (100,100,100), (xx, yy), (xx+100, yy), 2)

    pygame.draw.rect(screen, (200,200,200), pygame.Rect(-1000-my_Player.x+screen_x//2, -1000-my_Player.y+screen_y//2, 2000, 2000), 5)

    my_Player.draw()
    screen.blit(pygame.font.Font(None, 50).render(f'{int(my_Player.x)} : {int(my_Player.y)}', 1, (200,200,200)), (0, 0))

    for enemy_Player in enemy_Players:
        enemy_Player.draw(my_Player.x, my_Player.y)
        if my_Player.collide(enemy_Player.x, enemy_Player.y):
            my_Player.radius = ((3.14*(my_Player.radius**2) + 3.14*(enemy_Player.radius**2))/3.14)**0.5
            print(my_Player.radius)
            enemy_Players.remove(enemy_Player)
            enemy_Players.append(Enemy_Player(random.randint(-1000, 1000), random.randint(-1000, 1000), 10))




    mouse_x, mouse_y = pygame.mouse.get_pos()
    my_Player.x += min(200, max(-200, mouse_x - screen_x//2))/200
    my_Player.y += min(200, max(-200, mouse_y - screen_y//2))/200

    if my_Player.x+my_Player.radius > 1000: my_Player.x = 999-my_Player.radius
    if my_Player.x-my_Player.radius < -1000: my_Player.x = -999+my_Player.radius
    if my_Player.y+my_Player.radius > 1000: my_Player.y = 999-my_Player.radius
    if my_Player.y-my_Player.radius < -1000: my_Player.y = -999+my_Player.radius


    pygame.display.flip()
    clock.tick(120)
