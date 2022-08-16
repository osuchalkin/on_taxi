import pygame
from pygame.sprite import Sprite
import random


class Tile(Sprite):
    """Tile"""

    def __init__(self, image, rect, x, y):
        super().__init__()

        self.image = image
        self.rect = rect
        self.x, self.y = x, y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y


class Map(Sprite):
    """Карта"""

    def __init__(self):
        super().__init__()

        self.image_tiles = {'48': pygame.image.load('data/tiles/land_grass48.png'),
                            '75': pygame.image.load('data/tiles/road_asphalt75.png'),
                            '76': pygame.image.load('data/tiles/road_asphalt76.png'),
                            '93': pygame.image.load('data/tiles/road_asphalt93.png'),
                            '94': pygame.image.load('data/tiles/road_asphalt94.png'),
                            '130': pygame.image.load('data/tiles/road_asphalt130.png'),
                            '131': pygame.image.load('data/tiles/road_asphalt131.png'),
                            '148': pygame.image.load('data/tiles/road_asphalt148.png'),
                            '149': pygame.image.load('data/tiles/road_asphalt149.png'),
                            '166': pygame.image.load('data/tiles/road_asphalt166.png'),
                            '183': pygame.image.load('data/tiles/road_asphalt183.png'),
                            '184': pygame.image.load('data/tiles/road_asphalt184.png'),
                            '185': pygame.image.load('data/tiles/road_asphalt185.png'),
                            '202': pygame.image.load('data/tiles/road_asphalt202.png'),
                            '245': pygame.image.load('data/tiles/land_grass245.png'),
                            '253': pygame.image.load('data/tiles/road_asphalt253.png')
                            }

        self.image_objects = {'barrel1': pygame.image.load('data/objects/barrel_blue.png'),
                              'barrel2': pygame.image.load('data/objects/barrel_red.png'),
                              'rock1': pygame.image.load('data/objects/rock1.png'),
                              'rock2': pygame.image.load('data/objects/rock2.png'),
                              'rock3': pygame.image.load('data/objects/rock3.png'),
                              'tent1': pygame.image.load('data/objects/tent_blue.png'),
                              'tent2': pygame.image.load('data/objects/tent_red.png'),
                              'tree': pygame.image.load('data/objects/tree_small.png')}

        self.map_1 = self.get_map('data/map1.csv')

        self.tile_width = 128  # ширина 1 плитки в пикселях
        self.num_tiles = 100  # количество плиток по горизонтали и вертикали
        self.num_objects = 100  # количество объектов на карте
        self.tiles_group = pygame.sprite.Group()
        self.objects_group = pygame.sprite.Group()

    def get_map(self, filename):
        """
        This function loads an array based on a map stored as a list of
        numbers separated by commas.
        """
        map_file = open(filename)

        map_array = []

        for line in map_file:
            line = line.strip()
            map_row = line.split(",")  # создает список с помощью разделителя ","
            for index, item in enumerate(map_row):  # создает список int из str
                map_row[index] = int(item)

            map_array.append(map_row)  # добавляет список в список - получаем 2-мерный массив

        return map_array

    def decorate_map(self):
        """объекты на карте"""
        occupied_tile = set()
        keys = list(self.image_objects.keys())
        for i in range(0, self.num_objects):
            obj = str(random.choice(keys))
            obj_image = self.image_objects[obj]
            obj_rect = obj_image.get_rect()
            x = random.randint(0, self.num_tiles - 1)
            y = random.randint(0, self.num_tiles - 1)
            while self.map_1[y][x] not in (48, 245) and (x, y) not in occupied_tile:  # 48, 245 - тайлы травы
                x = random.randint(0, self.num_tiles - 1)
                y = random.randint(0, self.num_tiles - 1)
            occupied_tile.add((x, y))
            obj_x = x * self.tile_width + self.tile_width / 2
            obj_y = y * self.tile_width + self.tile_width / 2
            obj_rect.topleft = obj_x, obj_y
            new_obj = Tile(obj_image, obj_rect, obj_x, obj_y)
            self.objects_group.add(new_obj)

    def create_map(self):
        """создаем карту"""
        for x in range(0, self.num_tiles):
            for y in range(0, self.num_tiles):
                cell = str(self.map_1[x][y])
                image = self.image_tiles[cell]
                rect = image.get_rect()
                cell_x, cell_y = x * self.tile_width, y * self.tile_width
                tile = Tile(image, rect, cell_y, cell_x)
                self.tiles_group.add(tile)

        self.decorate_map()

    def update(self, x, y):
        """"""
        for tile in self.tiles_group:
            tile.update(x, y)
        for obj in self.objects_group:
            obj.update(x, y)
