import pygame
import neat
import time
import os
import random

from Base import Base
from Bird import Bird
from Consts import BG_IMAGE, WIN_WIDTH, WIN_HEIGHT, STAT_FONT
from Pipe import Pipe

GEN = 0


def draw_window(win, birds, pipes, base, score, generation, no_of_alive_birds):
    win.blit(BG_IMAGE, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    score_text = STAT_FONT.render("Score: "+str(score), 1, (255, 255, 255))
    win.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))

    generation_text = STAT_FONT.render("Generation: "+str(generation), 1, (255, 255, 255))
    win.blit(generation_text, (10, 10))

    alive_birds_text = STAT_FONT.render("Alive Birds: "+str(no_of_alive_birds), 1, (255, 255, 255))
    win.blit(alive_birds_text, (10, 40))

    pygame.display.update()



def main(genomes, config):
    global GEN
    nets = []
    ge = []
    birds = []
    GEN += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    score = 0

    run = True
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # move the birds
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                # if we have 2 pipes on the screen and the first bird passed the first pipe
                # calculate the distance from the second pipe, not the first one
                pipe_ind = 1
        else:
            run = False
            break
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            # activate the neural network
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        base.move()
        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird, win):
                    # collision detection
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
            for g in ge:
                # increase fitness more if it passes a pipe
                g.fitness += 5

        for p in rem:
            pipes.remove(p)

        for x, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                # hit the ground
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(win, birds, pipes, base, score, GEN, len(birds))
        if score > 50:
            break


def run(config_file_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 50)


if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "NEAT_Config.txt")
    run(config_path)

