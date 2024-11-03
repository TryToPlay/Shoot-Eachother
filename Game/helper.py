# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:25:13 2024.

@author: AVITA
"""

from PIL import Image
import pygame
import os


class Player():
    def __init__(self, image_list, bullet_image_list, width, height, x=0, y=0):
        self.sprite_dict = {"air_down_left": pygame.transform.scale(pygame.image.load(image_list[0]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "air_down_right": pygame.transform.scale(pygame.image.load(image_list[1]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "air_left": pygame.transform.scale(pygame.image.load(image_list[2]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "air_right": pygame.transform.scale(pygame.image.load(image_list[3]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "air_up_left": pygame.transform.scale(pygame.image.load(image_list[4]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "air_up_right": pygame.transform.scale(pygame.image.load(image_list[5]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "crouch_left": pygame.transform.scale(pygame.image.load(image_list[6]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "crouch_right": pygame.transform.scale(pygame.image.load(image_list[7]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "stand_left": pygame.transform.scale(pygame.image.load(image_list[8]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "stand_right": pygame.transform.scale(pygame.image.load(image_list[9]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "stand_up_left": pygame.transform.scale(pygame.image.load(image_list[10]).convert_alpha(), (width / 16 + 5, height / 9 + 5)),
                            "stand_up_right": pygame.transform.scale(pygame.image.load(image_list[11]).convert_alpha(), (width / 16 + 5, height / 9 + 5))
                            }
        self.facing = {"up": False, "left": False, "down": False, "right": True}
        self.x = x
        self.y = y

        self.crouching = False
        self.moving_left = True
        self.moving_right = True
        self.move_speed = width / 70
        self.fall_speed = height / 75
        self.jumping = False
        self.jump_speed = height / 50
        self.jump_count = 0
        self.jump_height = 15
        self.controls = {"up": False, "left": False, "down": False, "right": False, "jump": False, "shoot": False}

        self.hitbox = pygame.Rect(0, 0, width / 16, height / 9)
        self.hitbox.center = (self.x, self.y)
        self.top_rect = pygame.Rect(0, 0, self.hitbox.width, 1)
        self.top_rect.center = (self.hitbox.centerx, self.hitbox.top)
        self.left_rect = pygame.Rect(0, 0, 1, self.hitbox.height - self.fall_speed)
        self.left_rect.center = (self.hitbox.left, self.hitbox.centery)
        self.bottom_rect = pygame.Rect(0, 0, self.hitbox.width, 1)
        self.bottom_rect.center = (self.hitbox.centerx, self.hitbox.bottom)
        self.right_rect = pygame.Rect(0, 0, 1, self.hitbox.height - self.fall_speed)
        self.right_rect.center = (self.hitbox.right, self.hitbox.centery)

        self.bullet_sprite_dict = {"up": pygame.transform.scale(pygame.image.load(bullet_image_list[0]).convert_alpha(), (width / 128 + 5, height / 36 + 5)),
                                   "left": pygame.transform.scale(pygame.image.load(bullet_image_list[1]).convert_alpha(), (width / 64 + 5, height / 72 + 5)),
                                   "down": pygame.transform.scale(pygame.image.load(bullet_image_list[2]).convert_alpha(), (width / 128 + 5, height / 36 + 5)),
                                   "right": pygame.transform.scale(pygame.image.load(bullet_image_list[3]).convert_alpha(), (width / 64 + 5, height / 72 + 5))
                                   }
        self.bullet_list = []
        self.shooting_cooldown = 30
        self.shooting_timer = 0
        self.can_shoot = True
        self.shot = False

    def update_rects(self):
        self.top_rect = pygame.Rect(0, 0, self.hitbox.width, 1)
        self.top_rect.center = (self.hitbox.centerx, self.hitbox.top)
        self.left_rect = pygame.Rect(0, 0, 1, self.hitbox.height - self.fall_speed)
        self.left_rect.center = (self.hitbox.left, self.hitbox.centery)
        self.bottom_rect = pygame.Rect(0, 0, self.hitbox.width, 1)
        self.bottom_rect.center = (self.hitbox.centerx, self.hitbox.bottom)
        self.right_rect = pygame.Rect(0, 0, 1, self.hitbox.height - self.fall_speed)
        self.right_rect.center = (self.hitbox.right, self.hitbox.centery)

    def movement(self, level):
        for block in level.block_list:
            if self.left_rect.colliderect(block.hitbox):
                self.moving_left = False
                self.hitbox.left = block.hitbox.right
                break
        for block in level.block_list:
            if self.right_rect.colliderect(block.hitbox):
                self.moving_right = False
                self.hitbox.right = block.hitbox.left
                break
        if self.controls["left"] and self.moving_left:
            self.x -= self.move_speed
        if self.controls["right"] and self.moving_right:
            self.x += self.move_speed
        self.hitbox.centerx = self.x
        self.moving_left = True
        self.moving_right = True

    def fall(self, level):
        if not self.jumping and not self.is_on_block(level) and not self.crouching:
            self.y += self.fall_speed
        self.hitbox.centery = self.y

    def is_on_block(self, level):
        for block in level.block_list:
            if self.bottom_rect.colliderect(block.hitbox):
                self.hitbox.bottom = block.hitbox.top
                return True
        else:
            return False

    def jump(self, level):
        if self.is_on_block(level) and self.controls["jump"]:
            self.jumping = True
        for block in level.block_list:
            if self.top_rect.colliderect(block.hitbox):
                self.hitbox.top = block.hitbox.bottom
                self.jumping = False
                self.jump_count = 0
        if self.jumping:
            self.y -= self.jump_speed
            self.jump_count += 1
        if self.jump_count == self.jump_height:
            self.jump_count = 0
            self.jumping = False
        self.hitbox.centery = self.y

    def crouch(self, level):
        if self.is_on_block(level) and self.controls["down"]:
            temp = self.hitbox
            self.hitbox = pygame.Rect(0, 0, temp.width, temp.height / 2)
            self.hitbox.center = (temp.centerx, temp.centery + temp.height / 4 + 5)
            self.crouching = True
        if self.crouching and (self.controls["up"] or self.controls["left"] or self.controls["right"] or self.controls["jump"]):
            temp = self.hitbox
            self.hitbox = pygame.Rect(0, 0, temp.width, temp.height * 2)
            self.hitbox.center = (temp.centerx, temp.centery - temp.height / 4 - 5)
            self.crouching = False

    def looking_around(self, level):
        if self.controls["left"]:
            self.facing["left"] = True
            self.facing["right"] = False
        if self.controls["right"]:
            self.facing["right"] = True
            self.facing["left"] = False
        if self.controls["up"]:
            self.facing["up"] = True
        else:
            self.facing["up"] = False
        if not self.is_on_block(level) and self.controls["down"]:
            self.facing["down"] = True
        else:
            self.facing["down"] = False

    def display(self, window, level):
        if self.crouching:
            if self.facing["left"]:
                window.blit(self.sprite_dict["crouch_left"], self.hitbox)
            if self.facing["right"]:
                window.blit(self.sprite_dict["crouch_right"], self.hitbox)
        elif self.is_on_block(level):
            if self.facing["up"]:
                if self.facing["left"]:
                    window.blit(self.sprite_dict["stand_up_left"], self.hitbox)
                if self.facing["right"]:
                    window.blit(self.sprite_dict["stand_up_right"], self.hitbox)
            else:
                if self.facing["left"]:
                    window.blit(self.sprite_dict["stand_left"], self.hitbox)
                if self.facing["right"]:
                    window.blit(self.sprite_dict["stand_right"], self.hitbox)
        elif not self.is_on_block(level):
            if self.facing["up"]:
                if self.facing["left"]:
                    window.blit(self.sprite_dict["air_up_left"], self.hitbox)
                if self.facing["right"]:
                    window.blit(self.sprite_dict["air_up_right"], self.hitbox)
            if self.facing["down"]:
                if self.facing["left"]:
                    window.blit(self.sprite_dict["air_down_left"], self.hitbox)
                if self.facing["right"]:
                    window.blit(self.sprite_dict["air_down_right"], self.hitbox)
            if not (self.facing["up"] or self.facing["down"]):
                if self.facing["left"]:
                    window.blit(self.sprite_dict["air_left"], self.hitbox)
                if self.facing["right"]:
                    window.blit(self.sprite_dict["air_right"], self.hitbox)

        for bullet in self.bullet_list:
            window.blit(bullet.sprite, bullet.hitbox)

    def working(self, level, width, height, player_list):
        self.movement(level)
        self.update_rects()
        self.jump(level)
        self.update_rects()
        self.fall(level)
        self.update_rects()
        self.crouch(level)
        self.update_rects()
        self.looking_around(level)
        self.shooting(width, height)
        self.bullets_update(width, height, level)
        self.players_shot(player_list)

    def shooting(self, width, height):
        if self.can_shoot and self.controls["shoot"]:
            if self.facing["up"]:
                bullet = Bullet(self.bullet_sprite_dict["up"], width, height, self.top_rect.center, "up")
                self.bullet_list.append(bullet)
            elif self.facing["down"]:
                bullet = Bullet(self.bullet_sprite_dict["down"], width, height, self.bottom_rect.center, "down")
                self.bullet_list.append(bullet)
            else:
                if self.facing["left"]:
                    bullet = Bullet(self.bullet_sprite_dict["left"], width, height, self.left_rect.center, "left")
                    self.bullet_list.append(bullet)
                elif self.facing["right"]:
                    bullet = Bullet(self.bullet_sprite_dict["right"], width, height, self.right_rect.center, "right")
                    self.bullet_list.append(bullet)
            self.can_shoot = False

        if not self.can_shoot:
            self.shooting_timer += 1
            if self.shooting_timer >= self.shooting_cooldown:
                self.shooting_timer = 0
                self.can_shoot = True

    def bullets_update(self, width, height, level):
        bullets_to_remove = []
        for bullet in self.bullet_list:
            if bullet.dir == "up":
                bullet.hitbox.centery -= bullet.speed_y
            if bullet.dir == "left":
                bullet.hitbox.centerx -= bullet.speed_x
            if bullet.dir == "down":
                bullet.hitbox.centery += bullet.speed_y
            if bullet.dir == "right":
                bullet.hitbox.centerx += bullet.speed_x

            for block in level.block_list:
                if (bullet.hitbox.bottom <= 0) or (bullet.hitbox.right <= 0) or (bullet.hitbox.top >= height) or (bullet.hitbox.left >= width) or block.hitbox.colliderect(bullet.hitbox):
                    bullets_to_remove.append(bullet)
                    break
        
        for bullet in bullets_to_remove:
                self.bullet_list.remove(bullet)

    def players_shot(self, player_list):
        bullets_to_remove = []
        for bullet in self.bullet_list:
            for player in player_list:
                if self != player and player.hitbox.colliderect(bullet.hitbox) and not player.shot:
                    bullets_to_remove.append(bullet)
                    player.shot = True
        for bullet in bullets_to_remove:
                self.bullet_list.remove(bullet)


class Solid_block():
    def __init__(self, image, x=0, y=0):
        self.sprite = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (1, 1))
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(x, y, 1, 1)


class Solid_block2():
    def __init__(self, image, x, y, width, height):
        self.sprite = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
        self.hitbox = pygame.Rect(x, y, width, height)


class Level():
    def __init__(self, image, width, height):
        self.mapping = {"solid block": (0, 0, 0)}
        self.level_map = Image.open(image).resize((width, height)).load()
        self.block_list = [Solid_block("Assets" + os.sep + "Block_Sprites" + os.sep + "normal_block.png", x, y)
                           for x in range(width) for y in range(height) if self.level_map[x, y][:3] == self.mapping["solid block"]]


class Level2():
    def __init__(self, structure):
        self.block_list = []
        for block in structure:
            if block["type"] == "solid":
                rect = Solid_block2("Assets" + os.sep + "Block_Sprites" + os.sep + "normal_block.png",
                                   block["position"][0], block["position"][1], block["size"][0], block["size"][1])
                self.block_list.append(rect)


class Bullet():
    def __init__(self, sprite, width, height, start_position, direction):
        self.sprite = sprite
        self.hitbox = sprite.get_rect()
        self.hitbox.center = start_position
        self.speed_x = width / 40
        self.speed_y = height / 22.5
        self.dir = direction
