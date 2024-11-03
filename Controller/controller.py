# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 20:14:20 2024.

@author: AVITA
"""

import helper
import pygame
import socket
import sys
import os

pygame.init()
WIDTH = 800
HEIGHT = 450
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60

up_button = helper.Button("Assets" + os.sep + "up_button.png",
                          WIDTH, HEIGHT,
                          WIDTH / 4, HEIGHT / 5)
left_button = helper.Button("Assets" + os.sep + "left_button.png",
                            WIDTH, HEIGHT,
                            WIDTH / 8, HEIGHT / 2)
down_button = helper.Button("Assets" + os.sep + "down_button.png",
                            WIDTH, HEIGHT,
                            up_button.x, HEIGHT / (5 / 4))
right_button = helper.Button("Assets" + os.sep + "right_button.png",
                             WIDTH, HEIGHT,
                             WIDTH / (5 / 2), left_button.y)
jump_button = helper.Button("Assets" + os.sep + "jump_button.png",
                            WIDTH, HEIGHT,
                            WIDTH / (5 / 4), left_button.y)
shoot_button = helper.Button("Assets" + os.sep + "shoot_button.png",
                             WIDTH, HEIGHT,
                             jump_button.x, down_button.y)
button_list = [up_button, left_button, down_button,
               right_button, jump_button, shoot_button]

fingers = {}
inputs = up_button.pressed + left_button.pressed + down_button.pressed + right_button.pressed + jump_button.pressed + shoot_button.pressed

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostbyname(socket.gethostname()))
server_ip = "192.168.137.166"
server_port = 51083
client.connect((server_ip, server_port))

while True:
    if (WIDTH, HEIGHT) != window.get_size():
        WIDTH, HEIGHT = window.get_size()

        up_button = helper.Button("Assets" + os.sep + "up_button.png",
                                  WIDTH, HEIGHT,
                                  WIDTH / 4, HEIGHT / 5)
        left_button = helper.Button("Assets" + os.sep + "left_button.png",
                                    WIDTH, HEIGHT,
                                    WIDTH / 8, HEIGHT / 2)
        down_button = helper.Button("Assets" + os.sep + "down_button.png",
                                    WIDTH, HEIGHT,
                                    up_button.x, HEIGHT / (5 / 4))
        right_button = helper.Button("Assets" + os.sep + "right_button.png",
                                     WIDTH, HEIGHT,
                                     WIDTH / (5 / 2), left_button.y)
        jump_button = helper.Button("Assets" + os.sep + "jump_button.png",
                                    WIDTH, HEIGHT,
                                    WIDTH / (5 / 4), left_button.y)
        shoot_button = helper.Button("Assets" + os.sep + "shoot_button.png",
                                     WIDTH, HEIGHT,
                                     jump_button.x, down_button.y)
        button_list = [up_button, left_button, down_button,
                       right_button, jump_button, shoot_button]

    # Graphics

    window.fill((0, 0, 0))
    for button in button_list:
        window.blit(button.sprite, button.hitbox)

    # Events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.close()
            pygame.quit()
            sys.exit()

        if event.type == pygame.FINGERDOWN:
            x = event.x * WIDTH
            y = event.y * HEIGHT
            fingers[event.finger_id] = x, y
        if event.type == pygame.FINGERMOTION:
            for finger in fingers.keys():
                if finger == event.finger_id:
                    x = event.x * WIDTH
                    y = event.y * HEIGHT
                    fingers[finger] = x, y
        if event.type == pygame.FINGERUP:
            fingers.pop(event.finger_id, None)

    # Collisions

    for button in button_list:
        button.pressed = button.is_pressed(fingers)

    # Sending Inputs

    inputs = up_button.pressed + left_button.pressed + down_button.pressed + right_button.pressed + jump_button.pressed + shoot_button.pressed
    client.send(inputs.encode("utf-8"))

    # Screen Updates

    pygame.display.update()
    clock.tick(FPS)
