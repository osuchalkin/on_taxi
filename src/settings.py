import pygame
import random


class Settings:
    """класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        """
        # Screen settings
        self.screen_width = 1600
        self.screen_height = 1000
        # место машины
        self.center_x = self.screen_width / 2
        self.center_y = self.screen_height / 2
        """
        # для полноэкранного режима
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.center_x = int(pygame.display.Info().current_w / 2)
        self.center_y = int(pygame.display.Info().current_h / 2)

        self.bg_color = (39, 174, 96)

        self.caption = 'Race'
        self.icon = pygame.image.load('data/icon.png')

        self.fps = 90

        # количество машин в траффике
        self.traffic_count = 50

        # изображения человека и точки доставки
        self.targets = ['data/characters/character_black_blue.png',
                        'data/characters/character_black_green.png',
                        'data/characters/character_black_red.png',
                        'data/characters/character_black_white.png',
                        'data/characters/character_blonde_blue.png',
                        'data/characters/character_blonde_green.png',
                        'data/characters/character_blonde_red.png',
                        'data/characters/character_blonde_white.png',
                        'data/characters/character_brown_blue.png',
                        'data/characters/character_brown_green.png',
                        'data/characters/character_brown_red.png',
                        'data/characters/character_brown_white.png']
        self.target = self.targets[random.randint(0, len(self.targets)) - 1]
        self.destination = 'data/objects/cone_straight.png'

        # начальная статистика
        self.passengers = 0
        self.income = 0
        self.penalties = 0
        self.profit = 0

        # цены
        self.passenger = 5
        self.penalty_collide = 2

        # Таймер
        self.time = 5  # 5 минут игры
        self.countdown = self.fps * 60 * self.time
        self.timeleft = self.countdown

        self.penalty_cool = 270  # 3 секунды на столкновение

    def change_profit(self):
        """подсчет дохода"""
        self.profit = self.income - self.penalties
        return self.profit

    def update_time(self):
        """обновление таймера"""
        if self.timeleft > 0:
            self.timeleft -= 1

    def reset(self):
        """настройки для новой игры"""
        self.passengers = 0
        self.income = 0
        self.penalties = 0
        self.profit = 0

        self.timeleft = self.countdown
        self.penalty_cool = 270
