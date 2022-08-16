import pygame
from pygame.sprite import Sprite
import math


class Car(Sprite):
    """класс для управления автомобилем"""

    def __init__(self, game):
        """Инициализирует машину и задает ее начальную позицию."""
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.settings = game.settings

        self.image = pygame.image.load('data/cars/car_black_small_1.png')
        self.rect = self.image.get_rect()
        self.image_orig = self.image

        self.x = self.settings.center_x
        self.y = self.settings.center_y

        self.rect.topleft = self.x, self.y
        # начальная позиция машины - середина игрового поля
        self.x = 5900
        self.y = 5800

        # границы игрового поля
        self.bound_max_x = game.bound_max_x - self.rect.width
        self.bound_min_x = game.bound_min_x
        self.bound_max_y = game.bound_max_y - self.rect.height
        self.bound_min_y = game.bound_min_y

        # флаги перемещения
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        self.speed = 0.0
        self.maxspeed = 13.5
        self.minspeed = -1.85
        # если заехал в зеленую траву
        self.grass_speed = 0.715
        self.grass_green = 175

        self.dir = 0
        self.steering = 1.60
        self.acceleration = 0.095
        self.deacceleration = 0.12
        self.softening = 0.04

        self.penalty_cool = self.settings.penalty_cool

    def check_bounds(self):
        """проверка на достижение границы игрового поля"""
        if self.x > self.bound_max_x:
            self.x = self.bound_max_x
        if self.y > self.bound_max_y:
            self.y = self.bound_max_y
        if self.x < self.bound_min_x:
            self.x = self.bound_min_x
        if self.y < self.bound_min_y:
            self.y = self.bound_min_y

    def _rot_center(self, image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def blitme(self):
        """Рисует машину в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """обновляет позицию машины"""
        if self.moving_up:
            self.accelerate()
        else:
            self.soften()
        if self.moving_down:
            self.deaccelerate()
        if self.moving_left:
            self.steer_left()
        if self.moving_right:
            self.steer_right()
        self.image, self.rect = self._rot_center(self.image_orig, self.rect, self.dir)
        self.x = self.x + self.speed * math.cos(math.radians(270 - self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270 - self.dir))

        # отсчет времени столкновения - 3 секунды
        if self.penalty_cool > 0:
            self.penalty_cool -= 1

    def accelerate(self):
        """вперед с ускорением"""
        if self.speed < self.maxspeed:
            self.speed = self.speed + self.acceleration

    def soften(self):
        """езда с мягким торможением"""
        if self.speed > 0:
            self.speed -= self.softening
        if self.speed < 0:
            self.speed += self.softening

    def grass(self, value):
        """если заехал в траву - скорость падает.
        функция self.screen.get_at() возвращает color (RGB)
        функция self.screen.get_at().g возвращает возвращает значение G (value) из RGB"""
        if value < self.grass_green:
            if self.speed - self.deacceleration > self.grass_speed:
                self.speed = self.speed - self.deacceleration * 2

    def collision(self):
        """столкновение"""
        if self.speed > 0:
            self.speed = self.minspeed
        if self.penalty_cool == 0:
            self.settings.penalties += self.settings.penalty_collide
            self.penalty_cool = self.settings.penalty_cool

    def deaccelerate(self):
        """тормозим и на минималке едем назад"""
        if self.speed > self.minspeed:
            self.speed = self.speed - self.deacceleration

    def steer_left(self):
        """поворот налево"""
        self.dir = self.dir + self.steering
        if self.dir > 360:
            self.dir = 0

    def steer_right(self):
        """поворот направо"""
        self.dir = self.dir - self.steering
        if self.dir < 0:
            self.dir = 360
