import pygame
import neat
import time
import os
import random

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png"))),
]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 30)
