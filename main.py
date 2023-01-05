import pygame
import sys
from player import Player
import obstacle
from alien import Alien
import os
import time
import random


#
# pygame.font.init()
#
# WIDTH, HEIGHT = 750, 750
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Space Shooter Game")
#
# # Loading images
# RED_SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
# GREEN_SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
# BLUE_SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
#
# # Player ship
# PLAYER_SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
#
# # Lasers
#
# RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
# GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
# BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
# YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
#
# # Background
# BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
# class Ship:
#     def __init__(self, x, y, health=100):
#         self.x = x
#         self.y = y
#         # self.color = color
#         self.health = health
#         self.ship_img = None
#         self.laser_img = None
#         self.lasers = []
#         self.cool_down_counter = 0
#
#     def draw(self, widow):
#         pygame.draw.rect(WIN, (255, 0, 0), (self.x, self.y, 50, 50))
#
# def main():
#     run = True
#     FPS = 60
#     lvl = 1
#     lives = 5
#     main_font = pygame.font.SysFont("8-Bit-Madnes", 40)
#
#     ship = Ship(350, 650)
#
#     clock = pygame.time.Clock()
#
#     def redraw_window():
#         WIN.blit(BG, (0, 0))
#         # draw text
#         lives_label = main_font.render(f"LIVES: {lives}", 1, (255, 0, 0))
#         lvl_label = main_font.render(f"LVL: {lvl}", 1, (255, 255, 255))
#
#         WIN.blit(lives_label, (10, 10))
#         WIN.blit(lvl_label, (WIDTH - lvl_label.get_width() - 10, 10))
#         ship.draw(WIN)
#         pygame.display.update()
#
#     while run:
#         clock.tick(FPS)
#         redraw_window()
#
#         for event in pygame.event.get():
#
#             if event.type == pygame.QUIT:
#                 run = False
#
#
# main()

class Game:

    def __init__(self):
        player_sprite = Player((WIDTH / 2, HEIGHT), WIDTH, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=(WIDTH / 15), y_start=480)

        # alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)






    def create_obstacle(self, offset_x, x_start, y_start ):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(offset_x, x_start, y_start)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def run(self):
        WIN.blit(BG, (0, 0))

        self.player.update()

        self.player.sprite.lasers.draw(WIN)
        self.blocks.draw(WIN)
        self.player.draw(WIN)
        self.aliens.draw(WIN)


if __name__ == "__main__":

    pygame.init()
    WIDTH, HEIGHT = 750, 750
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    GAME = Game()
    FPS = 60
    BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WIN.fill((30, 30, 30))
        GAME.run()

        pygame.display.flip()
        CLOCK.tick(FPS)
