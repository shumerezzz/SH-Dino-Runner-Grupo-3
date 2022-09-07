import pygame
import random 

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            # self.obstacles.append(Cactus(SMALL_CACTUS))
            obstacle_type = random.randrange(1, 4)
            if obstacle_type == 1:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif obstacle_type == 2:
                self.obstacles.append(Cactus(LARGE_CACTUS))
            elif obstacle_type == 3:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)