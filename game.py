from datetime import datetime
from random import randint
import sys
import time
import pygame

pygame.init()

size = width, height = 500, 300

rect_width = width * 0.1
rect_height = width * 0.1

screen = pygame.display.set_mode(size)

score = 0

one_sec_since_epoch = 1000000000

coordinates = set()


def set_time_end(secs):
    return time.time_ns() + secs * one_sec_since_epoch


def seconds_left(time_end):
    return int((time_end - time.time_ns()) * 100 / one_sec_since_epoch)


def get_diffculty():
    if score >= 20:
        return "Hard"
    if score >= 10:
        return "Medium"
    if score > -1:
        return "Easy"


def populate_coordinates():
    for i in range(10):
        while 1:
            temp = (
                randint(0, width-rect_width),
                randint(50, height - rect_height),
                rect_width,
                rect_height
            )

            if temp not in coordinates:
                coordinates.add(temp)
                print(coordinates)
                break


def clicked(c, pos):
    return pos[0] > c[0] and pos[1] > c[1] and pos[0] < (c[0] + c[2]) and pos[1] < (c[1] + c[3])


def handle_level_end():
    global time_end
    if not coordinates:
        populate_coordinates()
        
        secs = None
        
        if score > 30:
            secs = 10
        else:
            secs = 60 - score
            
        time_end = set_time_end(secs)
        pass


time_end = set_time_end(60 - score)
populate_coordinates()

RUN = 1
while RUN:
    
    if seconds_left(time_end) == 0:
        break
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            for c in coordinates.copy():
                if clicked(c, pos):
                    score += 1
                    coordinates.remove(c)
                    handle_level_end()

    screen.fill((0, 0, 0))

    for c in coordinates:
        pygame.draw.rect(screen, (randint(0, 10), randint(0, 10), 255), c)

    screen.blit(
        pygame.font.Font.render(
            pygame.font.SysFont('Arial', 24),
            f"score {score}", 1, (0, 255, 0)),
        (0, 0)
    )

    screen.blit(
        pygame.font.Font.render(
            pygame.font.SysFont('Arial', 24),
            f"time left: {seconds_left(time_end)}", 1, (0, 255, 0)),
        (100, 0)
    )

    screen.blit(
        pygame.font.Font.render(
            pygame.font.SysFont('Arial', 24),
            f"Difficulty {get_diffculty()}", 1, (0, 255, 0)),
        (300, 0)
    )

    pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    screen.fill((0, 0, 0))
    
    screen.blit(
        pygame.font.Font.render(
            pygame.font.SysFont('Arial', 64),
            f"Your score is {score}", 1, (0, 0, 255)),
        (0, height/2)
    )
    
    pygame.display.flip()