'''
Created on Apr 8, 2014

@author: clear_000
'''

import pygame, sys
from pygame.locals import *

triangleLocation = (320, 240)
hlength = 25
speed = 50
dimensions = (640, 480)

pygame.init()
fpsClock = pygame.time.Clock()
whitecolor = pygame.Color(255, 255, 255)
blackcolor = pygame.Color(0, 0, 0)

window = pygame.display.set_mode(dimensions)

currvelo = (0, 0)

while True:
    x, y = triangleLocation
    velx, vely = currvelo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key in (K_UP, K_w):
                currvelo = (velx, vely-speed*0.1)
            if event.key in (K_LEFT, K_a):
                currvelo = (velx-speed*0.1, vely)
            if event.key in (K_RIGHT, K_d):
                currvelo = (velx+speed*0.1, vely)
            if event.key in (K_DOWN, K_s):
                currvelo = (velx, vely+speed*0.1)
        if event.type == KEYUP:
            if event.key in (K_UP, K_w):
                currvelo = (velx, vely+speed*0.1)
            if event.key in (K_LEFT, K_a):
                currvelo = (velx+speed*0.1, vely)
            if event.key in (K_RIGHT, K_d):
                currvelo = (velx-speed*0.1, vely)
            if event.key in (K_DOWN, K_s):
                currvelo = (velx, vely-speed*0.1)
    
    triangleLocation = (x+velx, y+vely)
    
    window.fill(blackcolor)
    pygame.draw.polygon(window, whitecolor, ((x+hlength, y+hlength), (x-hlength, y+hlength), (x, y-hlength)))
    pygame.display.update()
    fpsClock.tick(30)