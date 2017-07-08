#! /usr/bin/python3.5
''' game '''

import pygame

pygame.init()

game_display = pygame.display.set_mode((800,600))

pygame.display.set_caption('snek')

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        print(event)

pygame.display.update()

pygame.quit()
quit()