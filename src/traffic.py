import pygame
from pygame.sprite import Sprite
import random
import math


class Traffic(Sprite):
    """создает движение на дорогах"""

    def __init__(self, game):
        """Инициализирует машину и задает ее начальную позицию."""
        super().__init__()

        self.map = game.map

        self.car_files = ['data/cars/car_blue_small_1.png',
                          'data/cars/car_red_small_1.png',
                          'data/cars/car_green_small_1.png',
                          'data/cars/car_yellow_small_1.png',
                          'data/cars/car_blue_small_2.png',
                          'data/cars/car_red_small_2.png',
                          'data/cars/car_green_small_2.png',
                          'data/cars/car_yellow_small_2.png',
                          'data/cars/car_black_small_2.png',
                          'data/cars/car_blue_small_3.png',
                          'data/cars/car_red_small_3.png',
                          'data/cars/car_green_small_3.png',
                          'data/cars/car_yellow_small_3.png',
                          'data/cars/car_black_small_3.png',
                          'data/cars/car_blue_small_4.png',
                          'data/cars/car_red_small_4.png',
                          'data/cars/car_green_small_4.png',
                          'data/cars/car_yellow_small_4.png',
                          'data/cars/car_black_small_4.png',
                          'data/cars/car_blue_small_5.png',
                          'data/cars/car_red_small_5.png',
                          'data/cars/car_green_small_5.png',
                          'data/cars/car_yellow_small_5.png',
                          'data/cars/car_black_small_5.png'
                          ]

        self.cars = self.car_initialize()

        self.image = self.cars[random.randint(0, len(self.cars)) - 1]
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.x, self.y = self.road_tile()
        self.rect.topleft = self.x, self.y
        self.dir = 0
        self.speed = random.randint(60, 145) / 50
        self.collide_flag = False
        # тайл, на котором расположена машина
        self.tile = 0

    def car_initialize(self):
        """создает список машин"""
        cars = []
        for index in range(0, len(self.car_files)):
            cars.append(pygame.image.load(self.car_files[index]))
        return cars

    def road_tile(self):
        """определяет стартовое место машины и направление движения"""
        half_tile = self.map.tile_width / 2
        x = random.randint(0, self.map.num_tiles - 1)
        y = random.randint(0, self.map.num_tiles - 1)
        while self.map.map_1[x][y] != 184:  # 184 - тайл асфальта
            x = random.randint(0, self.map.num_tiles - 1)
            y = random.randint(0, self.map.num_tiles - 1)
        self.dir = random.choice((-90, 180, 90, 0))
        return y * self.map.tile_width - half_tile, x * self.map.tile_width - half_tile  # !! x = y, y = x

    def get_tile(self, x, y):
        """определяет координаты тайла"""
        tile_x = int(x // self.map.tile_width)
        tile_y = int(y // self.map.tile_width)
        return abs(tile_x), abs(tile_y)

    def check_tile(self, cur_x, cur_y):
        """update direction of traffic based on current tile"""
        tile_y, tile_x = self.get_tile(cur_x, cur_y)  # tile_y, tile_x = cur_x, cur_y !!
        if self.map.map_1[tile_x][tile_y] != self.tile:
            if self.map.map_1[tile_x][tile_y] in (48, 245):
                self.speed = 0
            if self.map.map_1[tile_x][tile_y] == 130:
                if self.dir == -90:
                    self.dir = 0
                if self.dir == 180:
                    self.dir = 90
            if self.map.map_1[tile_x][tile_y] == 131:
                if self.dir == -90:
                    self.dir = 180
                if self.dir == 0:
                    self.dir = 90
            if self.map.map_1[tile_x][tile_y] == 148:
                if self.dir == 180:
                    self.dir = -90
                if self.dir == 90:
                    self.dir = 0
            if self.map.map_1[tile_x][tile_y] == 149:
                if self.dir == 0:
                    self.dir = -90
                if self.dir == 90:
                    self.dir = 180
            if self.map.map_1[tile_x][tile_y] == 166:
                if self.dir == -90:
                    self.dir = random.choice((0, 180))
            if self.map.map_1[tile_x][tile_y] == 202:
                if self.dir == 90:
                    self.dir = random.choice((0, 180))
            if self.map.map_1[tile_x][tile_y] == 183:
                if self.dir == 180:
                    self.dir = random.choice((-90, 90))
            if self.map.map_1[tile_x][tile_y] == 185:
                if self.dir == 0:
                    self.dir = random.choice((-90, 90))

            self.tile = self.map.map_1[tile_x][tile_y]

    def _rot_center(self, image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def collide_cars(self):
        """обработка столкновения"""
        self.speed = -self.speed

        if self.dir == 0:
            self.dir = 180
        elif self.dir == 180:
            self.dir = 0
        elif self.dir == 90:
            self.dir = -90
        elif self.dir == -90:
            self.dir = 90

        self.speed = random.randint(60, 145) / 50

        self.collide_flag = False

    def update(self, cam_x, cam_y):
        """update moving of traffic based on current tile"""
        if self.collide_flag:
            self.collide_cars()
        self.check_tile(self.x, self.y)
        self.image, self.rect = self._rot_center(self.image_orig, self.rect, self.dir)
        self.x = self.x + self.speed * math.cos(math.radians(270 - self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270 - self.dir))

        self.rect.topleft = self.x - cam_x, self.y - cam_y
