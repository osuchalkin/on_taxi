# On Taxi 1.0
# (c) Oleh Suchalkin 2022

import sys

import pygame

from settings import Settings
from car import Car
from camera import Camera
from map import Map
from traffic import Traffic
from target import Target
from arrow import Arrow
from text import TextImage


class Game:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()  # для fps

        self.settings = Settings()
        """
        pygame.display.set_icon(self.settings.icon)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)
       

        """
        # полноэкранный режим
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.mouse.set_visible(False)

        self.text = TextImage(self)

        self.font = pygame.font.Font(None, 28)
        self.font_2 = pygame.font.Font(None, 42)
        self.font_color = (0, 0, 0)

        self.map = Map()
        # границы игрового поля
        self.bound_max_x = self.map.tile_width * self.map.num_tiles - self.settings.center_x
        self.bound_min_x = 0 - self.settings.center_x
        self.bound_max_y = self.map.tile_width * self.map.num_tiles - self.settings.center_y
        self.bound_min_y = 0 - self.settings.center_y

        self.car = Car(self)
        self.camera = Camera()
        self.traffics = pygame.sprite.Group()
        self.target = Target(self, self.settings.target)
        self.targets = pygame.sprite.Group()
        self.destination = Target(self, self.settings.destination)
        self.destinations = pygame.sprite.Group()
        self.get_target = False
        self.arrow = Arrow(self)

    def run_game(self):
        """запуск основного цикла"""
        self.start_screen()

        self.map.create_map()
        for count in range(0, self.settings.traffic_count):
            self.traffics.add(Traffic(self))
        self.targets.add(self.target)
        self.camera.set_position(self.car.x, self.car.y)

        while True:
            if self.settings.timeleft == 0:
                self.end_screen()
                self.new_game()
            else:
                self._check_events()
                self.camera.set_position(self.car.x, self.car.y)

                self._update_screen()

    def new_game(self):
        """новая игра"""
        self.settings.reset()
        del self.car
        del self.camera
        self.traffics.empty()
        del self.target
        self.targets.empty()
        del self.destination
        self.destinations.empty()
        del self.arrow

        self.car = Car(self)
        self.camera = Camera()
        self.traffics = pygame.sprite.Group()
        self.target = Target(self, self.settings.target)
        self.targets = pygame.sprite.Group()
        self.destination = Target(self, self.settings.destination)
        self.destinations = pygame.sprite.Group()
        self.get_target = False
        self.arrow = Arrow(self)
        for count in range(0, self.settings.traffic_count):
            self.traffics.add(Traffic(self))
        self.targets.add(self.target)
        self.camera.set_position(self.car.x, self.car.y)

    def _check_events(self):
        """Обрабатываем нажатия клавиш и мышь"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.car.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.car.moving_left = True
                elif event.key == pygame.K_UP:
                    self.car.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.car.moving_down = True
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.car.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.car.moving_left = False
                elif event.key == pygame.K_UP:
                    self.car.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.car.moving_down = False
                elif event.key == pygame.K_i:
                    # информация
                    self.screen.fill(self.settings.bg_color)
                    self.text.show_info_screen('On Taxi 1.0', self.text.info_text)

    def car_collide_objects(self):
        """проверка на столкновение машины игрока и машин траффика"""
        if pygame.sprite.spritecollide(self.car, self.map.objects_group, False):
            self.car.collision()

    def car_collide_traffics(self):
        """проверка на столкновение машины игрока и машин траффика"""
        car_hit = pygame.sprite.spritecollide(self.car, self.traffics, False)
        if car_hit:
            self.car.collision()
            for carh in car_hit:
                carh.collide_flag = True

    def collide_traffics(self):
        """проверка на столкновение машин траффика"""
        for car in self.traffics:
            self.traffics.remove(car)
            if pygame.sprite.spritecollide(car, self.traffics, False):
                car.collide_flag = True
            self.traffics.add(car)

    def collide_target(self):
        """нахождение цели"""
        if pygame.sprite.spritecollide(self.car, self.targets, True):
            self.get_target = True
            self.targets.empty()
            self.destination = Target(self, self.settings.destination)
            self.destinations.add(self.destination)
        if pygame.sprite.spritecollide(self.car, self.destinations, True):
            self.get_target = False
            self.destinations.empty()
            self.target = Target(self, self.settings.target)
            self.targets.add(self.target)
            self.settings.passengers += 1
            self.settings.income += self.settings.passenger

    def _update_map(self):
        self.map.update(self.camera.x, self.camera.y)
        self.map.tiles_group.draw(self.screen)
        self.map.objects_group.draw(self.screen)

    def _update_collide(self):
        self.car_collide_traffics()
        self.collide_traffics()
        self.collide_target()
        self.car_collide_objects()

    def _update_car(self):
        self.car.check_bounds()
        self.car.grass(self.screen.get_at((int(self.settings.center_x - 5), int(self.settings.center_y - 5))).g)
        self.car.update()
        self.car.blitme()

    def _update_traffics(self):
        self.traffics.update(self.camera.x, self.camera.y)
        self.traffics.draw(self.screen)

    def _update_target_and_destination(self):
        self.targets.update(self.camera.x, self.camera.y)
        self.targets.draw(self.screen)
        self.destinations.update(self.camera.x, self.camera.y)
        self.destinations.draw(self.screen)

    def _update_arrow(self):
        if self.get_target:
            self.arrow.update(self.car.x + self.settings.center_x,
                              self.car.y + self.settings.center_y,
                              self.destination.x, self.destination.y)
        else:
            self.arrow.update(self.car.x + self.settings.center_x,
                              self.car.y + self.settings.center_y,
                              self.target.x, self.target.y)
        self.arrow.blitme()

    def _update_screen(self):
        """Обновляет изображения на экране"""
        self.screen.fill(self.settings.bg_color)

        self._update_map()
        self._update_collide()
        self._update_car()
        self._update_traffics()
        self._update_target_and_destination()
        self._update_arrow()
        self.settings.update_time()
        self.show_status()
        pygame.display.flip()

        # скорость
        self.clock.tick(self.settings.fps)

    def end_screen(self):
        """конец игры"""
        msg = ''
        profit = self.settings.change_profit()
        if 0 < profit <= 10:
            msg = 'Not bad'
        elif 10 < profit <= 20:
            msg = 'Very good'
        elif profit > 20:
            msg = 'Great!'
        elif profit < 0:
            msg = 'Very sad'
        instructions = ['Your time is up',
                        f'Your profit {profit}',
                        msg,
                        'Press SPACE key to start new game']

        top_coord = self.settings.screen_height / 2 - 200
        for i in range(len(instructions)):
            inst_surf = self.font_2.render(instructions[i], True, self.font_color)
            inst_rect = inst_surf.get_rect()
            top_coord += 10  # 10 pixels will go in between each line of text.
            inst_rect.top = top_coord
            inst_rect.centerx = self.settings.screen_width / 2
            top_coord += inst_rect.height  # Adjust for the height of the line.
            self.screen.blit(inst_surf, inst_rect)

        while True:  # Main loop for the end screen.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        return  # user has pressed a key, so return.
            pygame.display.flip()

    def start_screen(self):
        """стартовый экран"""
        image = pygame.image.load('data/start.png')
        title_image = pygame.transform.scale(image, (self.settings.screen_width, self.settings.screen_height))
        title_rect = title_image.get_rect()
        self.screen.blit(title_image, title_rect)

        instructions = ['Pick up a passenger and take him to the destination (cone).',
                        'Arrow keys to move.',
                        'Q or Esc - quit.']

        top_coord = self.settings.screen_height / 2 + 100
        for i in range(len(instructions)):
            inst_surf = self.font.render(instructions[i], True, (255, 255, 255))
            inst_rect = inst_surf.get_rect()
            top_coord += 10  # 10 pixels will go in between each line of text.
            inst_rect.top = top_coord
            inst_rect.centerx = self.settings.screen_width / 2
            top_coord += inst_rect.height  # Adjust for the height of the line.
            self.screen.blit(inst_surf, inst_rect)

        while True:  # Main loop for the start screen.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    return  # user has pressed a key, so return.
            pygame.display.flip()

    def show_status(self):
        """"""
        text_timer = self.font.render('Timer: ' +
                                      str(int((self.settings.timeleft / self.settings.fps) / 60)) + ":"
                                      + str(int((self.settings.timeleft / self.settings.fps) % 60)),
                                      True, self.font_color)
        textpos_timer = text_timer.get_rect(y=25, x=30)

        text_passengers = self.font.render('Passengers: ' + str(self.settings.passengers), True, self.font_color)
        textpos_passengers = text_passengers.get_rect(y=55, x=30)

        text_income = self.font.render('Income: ' + str(self.settings.income), True, self.font_color)
        textpos_income = text_income.get_rect(y=85, x=30)

        text_penalty = self.font.render('Penalties: ' + str(self.settings.penalties), True, self.font_color)
        textpos_penalty = text_penalty.get_rect(y=115, x=30)

        text_profit = self.font.render('Profit: ' + str(self.settings.change_profit()), True, self.font_color)
        textpos_profit = text_profit.get_rect(y=145, x=30)

        self.screen.blit(text_timer, textpos_timer)
        self.screen.blit(text_passengers, textpos_passengers)
        self.screen.blit(text_income, textpos_income)
        self.screen.blit(text_penalty, textpos_penalty)
        self.screen.blit(text_profit, textpos_profit)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
