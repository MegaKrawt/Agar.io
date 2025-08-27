import ast
import math
import time
from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('26.123.126.212', 55555))
server_socket.setblocking(False)
server_socket.listen(5)
clients = []

class My_Player():
    def __init__(self, p):
        self.radius = p[2]
        self.y = p[1]
        self.x = p[0]

    def collide(self, x, y):
        distans = math.hypot(self.x - x, self.y - y)
        return (distans < self.radius)

players = dict()
while True:
    time.sleep(0.005)
    try:
        connection, address = server_socket.accept()
        print (f'Підключився клієнт {connection}')
        connection.setblocking(True)
        clients.append(connection)
        a = str(connection).split('), ')[1][0:-1]
        players[a] = ast.literal_eval(connection.recv(1024).decode())
        connection.setblocking(False)
    except : pass



    to_remove = []
    for client in clients:
        try:
            a = str(client).split('), ')[1][0:-1]
            players[a] = ast.literal_eval(client.recv(1024).decode())
        except: pass
    if players != {}:
        print(players)

    for p in players.items():
        for p2 in players.items():
            if p != p2:
                if My_Player(p[1]).collide(p2[1][0], p2[1][1]):
                    My_radius = ((3.14 * (p[1][2] ** 2) + 3.14 * (p2[1][2] ** 2)) / 3.14) ** 0.5
                    players[p[0]][2] = My_radius
                    to_remove.append(p2)

    for i in to_remove:
        del players[i[0]]

    for client in clients:
        try:
            client.send((str(players)+'&').encode())
        except:
            try:
                clients.remove(client)
                a = str(client).split('), ')[1][0:-1]
                del players[a]
            except: pass

