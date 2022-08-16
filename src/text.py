import pygame.font
import pygame
import sys


class TextImage:
    """для вывода текстовой информации"""

    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.text_color = (58, 53, 53)
        self.text_shadow_color = (41, 37, 37)

        self.small_font = pygame.font.Font(None, 40)
        self.big_font = pygame.font.Font(None, 100)
        self.info_font = pygame.font.Font(None, 30)

        self.info_text = ['This game is clone Race-game created Robin Duda in 2012-15 (License MIT).',
                          '',
                          'Racing Pack created/distributed by Kenney (www.kenney.nl)',
                          'License: Creative Commons Zero, CC0',
                          '',
                          '© Oleh Suchalkin 2022']

    def make_text_obj(self, text, font, text_color):
        image = font.render(text, True, text_color)
        image_rect = image.get_rect()
        return image, image_rect

    def check_for_keypress(self):
        """ожидает события KEYUP"""
        # проверка на выход из програмы (Х или ESC)
        self.check_for_quit()
        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            if event == pygame.KEYDOWN:
                continue
            return event.key
        return None

    def check_for_quit(self):
        for event in pygame.event.get(pygame.QUIT):  # get all the QUIT event
            pygame.quit()
            sys.exit()

    def show_info_screen(self, title, text):
        """показывает информационный текст"""
        # рисует тень
        title_screen, title_rect = self.make_text_obj(title, self.big_font, self.text_shadow_color)
        title_rect.center = (int(self.settings.screen_width / 2), 100)
        self.screen.blit(title_screen, title_rect)

        # рисует текст
        title_screen, title_rect = self.make_text_obj(title, self.big_font, self.text_color)
        title_rect.center = (int(self.settings.screen_width / 2) - 3, 100 - 3)
        self.screen.blit(title_screen, title_rect)

        i = 1
        for info in text:
            title_screen, title_rect = self.make_text_obj(info, self.info_font, self.text_color)
            title_rect.center = (int(self.settings.screen_width / 2), 300 + 30 * i)
            self.screen.blit(title_screen, title_rect)
            i += 1

        # рисуем "Press a key to play"
        presskey_screen, presskey_rect = self.make_text_obj('Press a key to play', self.small_font, self.text_color)
        presskey_rect.center = (int(self.settings.screen_width / 2),
                                int(self.settings.screen_height / 2) + 300)
        self.screen.blit(presskey_screen, presskey_rect)

        while self.check_for_keypress() is None:
            pygame.display.flip()
