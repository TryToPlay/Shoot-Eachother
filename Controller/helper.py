# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 21:10:35 2024.

@author: AVITA
"""

import pygame
import socket


class Button():
    def __init__(self, image, width, height, x, y):
        self.sprite = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width / 5, height / 4))
        self.hitbox = pygame.Rect(0, 0, width / 5, height / 4)
        self.x = x
        self.y = y
        self.hitbox.center = (self.x, self.y)
        self.pressed = 'f'

    def is_pressed(self, fingers):
        for finger, pos in fingers.items():
            if self.hitbox.collidepoint(pos):
                self.sprite.set_alpha(175)
                return 't'
        else:
            self.sprite.set_alpha(255)
            return 'f'


def find_ip(client_socket):
    pass
