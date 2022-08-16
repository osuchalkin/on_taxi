import pygame
import math
from pygame.sprite import Sprite


class Arrow(Sprite):
    """Указатель цели"""

    def __init__(self, game):
        super().__init__()

        self.settings = game.settings
        self.screen = game.screen
        self.image_orig = pygame.image.load('data/objects/arrow.png')
        self.image_orig = pygame.transform.scale(self.image_orig, (90, 90))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect_orig = self.rect
        # координаты стрелки
        self.x = self.settings.screen_width / 2
        self.y = 50

        self.rect.topleft = self.x, self.y
        self.dir = 0

    def _rotate(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def update(self, point_x, point_y, target_x, target_y):
        self.dir = (math.atan2(point_y - target_y, target_x - point_x) * 180 / math.pi)
        self.image, self.rect = self._rotate(self.image_orig, self.rect_orig, self.dir)

    def blitme(self):
        """Рисует стрелку"""
        self.screen.blit(self.image, self.rect)
