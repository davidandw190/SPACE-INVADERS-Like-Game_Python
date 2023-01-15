import pygame
import sys
from player import Player
import obstacle
from alien import Alien, Extra
import os
from random import choice, randint
from laser import Laser


class Game:

    def __init__(self):
        # Player setup
        player_sprite = Player((WIDTH / 2, HEIGHT), WIDTH)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health & Score setup
        self.lives = 3
        self.live_surface = pygame.image.load("graphics/player.png").convert_alpha()
        self.live_x_start_pos = WIDTH - (self.live_surface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font("font/Pixelated.ttf", 20)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=(WIDTH / 15), y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(300, 600)

        # Audio
        music = pygame.mixer.Sound("audio/music.wav")
        music.set_volume(0.2)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound("audio/laser.wav")
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound("audio/explosion.wav")
        self.explosion_sound.set_volume(0.3)

    def create_obstacle(self, offset_x, x_start, y_start):
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

    def alien_position_check(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= WIDTH:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance: int):
        all_aliens = self.aliens.sprites()
        if self.aliens:
            for alien in all_aliens:
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, -7, HEIGHT)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(["right", "left"]), WIDTH))

    def collision_check(self):

        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:

                # Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # Alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # Extra collisions
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()

        # Alien lasers
        if self.alien_lasers:
            for alien_laser in self.alien_lasers:

                # Obstacle collisions
                if pygame.sprite.spritecollide(alien_laser, self.blocks, True):
                    alien_laser.kill()

                if pygame.sprite.spritecollide(alien_laser, self.player, False):
                    alien_laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # Aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + live * (self.live_surface.get_size()[0] + 20)
            WIN.blit(self.live_surface, (x, 8))

    def display_score(self):
        score_surface = self.font.render(f"SCORE: {self.score}", False, "white")
        score_rect = score_surface.get_rect(topleft=(10, -10))
        WIN.blit(score_surface, score_rect)

    def display_victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render("You won", False, "white")
            victory_rect = victory_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            WIN.blit(victory_surf, victory_rect)

    def run(self):
        # Display background on window
        WIN.blit(BG, (0, 0))

        # Basic updates
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()

        # Additional Updates
        self.aliens.update(self.alien_direction)
        self.alien_position_check()
        self.extra_alien_timer()
        self.collision_check()

        # Display onto the window
        self.player.sprite.lasers.draw(WIN)
        self.player.draw(WIN)
        self.blocks.draw(WIN)
        self.aliens.draw(WIN)
        self.alien_lasers.draw(WIN)
        self.extra.draw(WIN)
        self.display_lives()
        self.display_score()
        self.display_victory_message()


class CRT:
    def __init__(self):
        self.tv = pygame.image.load("graphics/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (WIDTH, HEIGHT))

    def create_crt_lines(self):
        crt_line_height = 3
        crt_line_amount = int(HEIGHT / crt_line_height)
        for line in range(crt_line_amount):
            y_pos = line * crt_line_height
            pygame.draw.line(self.tv, "black", (0, y_pos), (WIDTH, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        WIN.blit(self.tv, (0, 0))


if __name__ == "__main__":

    pygame.init()
    WIDTH, HEIGHT = 750, 750
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    GAME = Game()
    CRT = CRT()
    FPS = 60

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == ALIENLASER:
                GAME.alien_shoot()

        WIN.fill((30, 30, 30))
        GAME.run()
        CRT.draw()

        pygame.display.flip()
        CLOCK.tick(FPS)
