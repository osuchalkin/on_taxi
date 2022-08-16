import pygame
from pygame.sprite import Sprite
import random


class Target(Sprite):
    """цель, к которой едет машина"""

    def __init__(self, game, image_name):
        super().__init__()

        self.map = game.map
        self.image_name = image_name
        self.x = 5
        self.y = 5
        self.target_initialize()
        self.generate_target()

    def target_initialize(self):
        """"""
        self.image = pygame.image.load(self.image_name)
        if self.image_name == 'data/objects/cone_straight.png':
            pass
        else:
            self.image = pygame.transform.scale(self.image, (26, 18))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def generate_target(self):
        """случайным образом определяет место цели на карте"""
        x = random.randint(0, self.map.num_tiles - 1)
        y = random.randint(0, self.map.num_tiles - 1)
        while self.map.map_1[y][x] != 184:  # 184 - тайл асфальта
            x = random.randint(0, self.map.num_tiles - 1)
            y = random.randint(0, self.map.num_tiles - 1)
        self.x = x * self.map.tile_width + self.map.tile_width / 2
        self.y = y * self.map.tile_width + self.map.tile_width / 2
        self.rect.topleft = self.x, self.y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
