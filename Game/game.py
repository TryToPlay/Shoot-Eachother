# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:24:19 2024.

@author: AVITA
"""

import helper
import pygame
import socket
import time
import sys
import os

pygame.init()
WIDTH = 400
HEIGHT = 225
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot Eachother")
clock = pygame.time.Clock()
FPS = 60

number_of_players = 1
player_sprite_dict_list = [["Assets" + os.sep + "Player_Sprites" + os.sep + "air_down_left.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "air_down_right.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "air_left.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "air_right.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "air_up_left.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "air_up_right.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "crouch_left.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "crouch_right.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "stand_left.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "stand_right.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "stand_up_left.png",
                            "Assets" + os.sep + "Player_Sprites" + os.sep + "stand_up_right.png"]] * number_of_players
player_list = []

bullet_sprite_dict_list = [["Assets" + os.sep + "Bullet_Sprites" + os.sep + "bullet_up.png",
                            "Assets" + os.sep + "Bullet_Sprites" + os.sep + "bullet_left.png",
                            "Assets" + os.sep + "Bullet_Sprites" + os.sep + "bullet_down.png",
                            "Assets" + os.sep + "Bullet_Sprites" + os.sep + "bullet_right.png"]] * number_of_players

for i in range(number_of_players):
    player = helper.Player(player_sprite_dict_list[i],
                           bullet_sprite_dict_list[i],
                           WIDTH, HEIGHT,
                           WIDTH / 2, HEIGHT / 2)
    player_list.append(player)

level_structure = [{"size": ((WIDTH / 400) * 400, (HEIGHT / 225) * 50),"position": ((WIDTH / 400) * 0, (HEIGHT / 225) * 175), "type": "solid"},
                   {"size": ((WIDTH / 400) * 100, (HEIGHT / 225) * 25),"position": ((WIDTH / 400) * 25, (HEIGHT / 225) * 125), "type": "solid"},
                   {"size": ((WIDTH / 400) * 100, (HEIGHT / 225) * 25),"position": ((WIDTH / 400) * 275, (HEIGHT / 225) * 125), "type": "solid"}]

print("Level Processing Started")
t1 = time.time()
level = helper.Level2(level_structure)
t2 = time.time()
print(f"Time Taken For Level Processing: {t2-t1}")

server_ip = ""
port = 51083
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, port))
server.listen(number_of_players)
client_sockets = []
print("Waiting For Controller(s)...")

for i in range(number_of_players):
    client_socket, client_address = server.accept()
    client_sockets.append(client_socket)
    print(f"Connected Players: {i + 1}")
print("All Players Connected")
inputs_list = []

while True:
    # Graphics

    window.fill((255, 255, 255))

    for player in player_list:
        player.display(window, level)
        if not player.shot:
            player.working(level, WIDTH, HEIGHT, player_list)

    for block in level.block_list:
        window.blit(block.sprite, block.hitbox)

    # Events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server.close()
            pygame.quit()
            sys.exit()

    # Receiving Inputs

    for client_socket in client_sockets:
        inputs = client_socket.recv(1024).decode("utf-8")[:6]
        inputs_list.append(inputs)
    for i in range(number_of_players):
        if inputs_list[i][0] == 't':
            player_list[i].controls["up"] = True
        elif inputs_list[i][0] == 'f':
               player_list[i].controls["up"] = False
        if inputs_list[i][1] == 't':
            player_list[i].controls["left"] = True
        elif inputs_list[i][1] == 'f':
            player_list[i].controls["left"] = False
        if inputs_list[i][2] == 't':
            player_list[i].controls["down"] = True
        elif inputs_list[i][2] == 'f':
            player_list[i].controls["down"] = False
        if inputs_list[i][3] == 't':
            player_list[i].controls["right"] = True
        elif inputs_list[i][3] == 'f':
            player_list[i].controls["right"] = False
        if inputs_list[i][4] == 't':
            player_list[i].controls["jump"] = True
        elif inputs_list[i][4] == 'f':
            player_list[i].controls["jump"] = False
        if inputs_list[i][5] == 't':
            player_list[i].controls["shoot"] = True
        elif inputs_list[i][5] == 'f':
            player_list[i].controls["shoot"] = False
    inputs_list = []

    pygame.display.update()
    clock.tick(FPS)
