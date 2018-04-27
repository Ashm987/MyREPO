import pygame
import sys
import math
import random
import time
from pygame.locals import *
pygame.init()

'''DIRECTIONS:
   1: Up
   2: Left
   3: Down
   4: Right'''

try:
    screen = pygame.display.set_mode((736, 813))
    clock = pygame.time.Clock()

    board = pygame.image.load(sys.path[0] + '/imgs/board.jpeg')
    player = pygame.image.load(sys.path[0] + '/imgs/player.png')
    ghost1 = pygame.image.load(sys.path[0] + '/imgs/ghost1.png')
    ghost2 = pygame.image.load(sys.path[0] + '/imgs/ghost2.png')
    ghost3 = pygame.image.load(sys.path[0] + '/imgs/ghost3.png')
    pellet = pygame.image.load(sys.path[0] + '/imgs/pellet.png')
    power_pellet = pygame.image.load(sys.path[0] + '/imgs/power_pellet.png')
    icon = pygame.image.load(sys.path[0] + '/imgs/icon.ico')

    sprite_vars = {player: {'speed': 2.5, 'pos': (230, 200)}, ghost1: {'speed': 1, 'pos': (290, 360), 'roaming': False}, ghost2: {
        'speed': 1, 'pos': (345, 360), 'roaming': False}, ghost3: {'speed': 1, 'pos': (395, 360), 'roaming': False}}

    score = -20
    level = 0

    pygame.display.set_icon(icon)

    intersections = {(20, 20): (1, 4), (150, 20): (0, 1), (305, 20): (1, 2), (390, 20): (1, 4), (545, 20): (0, 1), (670, 20): (1, 2),
                     (20, 120): (0, 4), (150, 120): (0, 5), (230, 120): (0, 1), (305, 120): (0, 3), (390, 120): (0, 3), (465, 120): (0, 1), (545, 120): (0, 5), (670, 120): (0, 2),
                     (20, 200): (3, 4), (150, 200): (0, 2), (230, 200): (3, 4), (305, 200): (1, 2), (390, 200): (1, 4), (465, 200): (2, 3), (545, 200): (0, 5), (670, 200): (2, 3),
                     (230, 280): (1, 4), (305, 280): (0, 3), (390, 280): (0, 3), (465, 280): (1, 2),
                     (150, 360): (0, 5), (230, 360): (0, 2), (465, 360): (0, 4), (545, 360): (0, 5),
                     (230, 435): (0, 4), (465, 435): (0, 2),
                     (20, 510): (1, 4), (150, 510): (0, 5), (230, 510): (0, 3), (305, 510): (1, 2), (390, 510): (1, 4), (465, 510): (0, 3), (545, 510): (0, 5), (670, 510): (1, 2),
                     (20, 595): (3, 4), (70, 595): (1, 2), (150, 595): (0, 4), (230, 595): (0, 1), (305, 595): (0, 3), (390, 595): (0, 3), (465, 595): (0, 1), (545, 595): (0, 2), (620, 595): (1, 4), (670, 595): (2, 3),
                     (20, 665): (3, 4), (70, 665): (0, 3), (150, 665): (2, 3), (230, 665): (3, 4), (305, 665): (1, 2), (390, 665): (1, 4), (465, 665): (2, 3), (545, 665): (3, 4), (620, 665): (0, 3), (670, 665): (1, 2),
                     (20, 750): (3, 4), (305, 750): (0, 3), (390, 750): (0, 3), (670, 750): (2, 3)}


    player_move_dir = 0
    pellet_enabled = False

    pellets = []


    def ghost_move(ghost):
        #global ghost_move_dir
        if sprite_vars[ghost]['roaming']:
            if sprite_vars[ghost]['pos'] in intersections:
                ghost_move_dir = random.randint(1, 4)
                if ghost_move_dir not in intersections[sprite_vars[ghost]['pos']]:
                    if ghost_move_dir == 1:
                        v = list(sprite_vars[ghost]['pos'])
                        v[1] -= sprite_vars[ghost]['speed']
                        sprite_vars[ghost]['pos'] = tuple(v)
                    if ghost_move_dir == 2:
                        v = list(sprite_vars[ghost]['pos'])
                        v[0] += sprite_vars[ghost]['speed']
                        sprite_vars[ghost]['pos'] = tuple(v)
                    if ghost_move_dir == 3:
                        v = list(sprite_vars[ghost]['pos'])
                        v[1] += sprite_vars[ghost]['speed']
                        sprite_vars[ghost]['pos'] = tuple(v)
                    if ghost_move_dir == 4:
                        v = list(sprite_vars[ghost]['pos'])
                        v[0] -= sprite_vars[ghost]['speed']
                        sprite_vars[ghost]['pos'] = tuple(v)
            else:
                if ghost_move_dir == 1:
                    v = list(sprite_vars[ghost]['pos'])
                    v[1] -= sprite_vars[ghost]['speed']
                    sprite_vars[ghost]['pos'] = tuple(v)
                if ghost_move_dir == 2:
                    v = list(sprite_vars[ghost]['pos'])
                    v[0] += sprite_vars[ghost]['speed']
                    sprite_vars[ghost]['pos'] = tuple(v)
                if ghost_move_dir == 3:
                    v = list(sprite_vars[ghost]['pos'])
                    v[1] += sprite_vars[ghost]['speed']
                    sprite_vars[ghost]['pos'] = tuple(v)
                if ghost_move_dir == 4:
                    v = list(sprite_vars[ghost]['pos'])
                    v[0] -= sprite_vars[ghost]['speed']
                    sprite_vars[ghost]['pos'] = tuple(v)
        else:
            while sprite_vars[ghost]['pos'][0] > 345:
                v = list(sprite_vars[ghost]['pos'])
                v[0] -= sprite_vars[ghost]['speed']
                sprite_vars[ghost]['pos'] = tuple(v)
            while sprite_vars[ghost]['pos'][0] < 345:
                v = list(sprite_vars[ghost]['pos'])
                v[0] += sprite_vars[ghost]['speed']
                sprite_vars[ghost]['pos'] = tuple(v)
            while sprite_vars[ghost]['pos'][1] > 280:
                v = list(sprite_vars[ghost]['pos'])
                v[1] -= sprite_vars[ghost]['speed']
                sprite_vars[ghost]['pos'] = tuple(v)
            if random.randint(0, 1) == 0:
                while sprite_vars[ghost]['pos'][0] > 305:
                    v = list(sprite_vars[ghost]['pos'])
                    v[0] -= sprite_vars[ghost]['speed']
                    sprite_vars[ghost]['pos'] = tuple(v)
            else:
                while sprite_vars[ghost]['pos'][0] < 390:
                    v = list(sprite_vars[ghost]['pos'])
                    v[0] += sprite_vars[ghost]['speed']
                    sprite_vars[ghost]['pos'] = tuple(v)
            sprite_vars[ghost]['roaming'] = True


    while True:
        init_sprite_vars = {player: {'speed': 2.5, 'pos': (230, 200)}, ghost1: {'speed': 1, 'pos': (290, 360), 'roaming': False}, ghost2: {
            'speed': 1, 'pos': (345, 360), 'roaming': False}, ghost3: {'speed': 1, 'pos': (395, 360), 'roaming': False}}

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if sprite_vars[player]['pos'] in intersections:
                if event.type == pygame.KEYDOWN:
                    if event.key in [119, 273] and 1 not in intersections[sprite_vars[player]['pos']]:
                        player_move_dir = 1
                        v = list(sprite_vars[player]['pos'])
                        v[1] -= sprite_vars[player]['speed']
                        sprite_vars[player]['pos'] = tuple(v)

                    if event.key in [100, 275] and 2 not in intersections[sprite_vars[player]['pos']]:
                        player_move_dir = 2
                        v = list(sprite_vars[player]['pos'])
                        v[0] += sprite_vars[player]['speed']
                        sprite_vars[player]['pos'] = tuple(v)

                    if event.key in [115, 274] and 3 not in intersections[sprite_vars[player]['pos']]:
                        player_move_dir = 3
                        v = list(sprite_vars[player]['pos'])
                        v[1] += sprite_vars[player]['speed']
                        sprite_vars[player]['pos'] = tuple(v)

                    if event.key in [97, 276] and 4 not in intersections[sprite_vars[player]['pos']]:
                        player_move_dir = 4
                        v = list(sprite_vars[player]['pos'])
                        v[0] -= sprite_vars[player]['speed']
                        sprite_vars[player]['pos'] = tuple(v)

        screen.blit(board, (0, 0))
        for sprite in sprite_vars:
            screen.blit(sprite, sprite_vars[sprite]['pos'])


        if sprite_vars[player]['pos'] not in intersections:
            if player_move_dir == 1:
                v = list(sprite_vars[player]['pos'])
                v[1] -= sprite_vars[player]['speed']
                sprite_vars[player]['pos'] = tuple(v)
            if player_move_dir == 2:
                v = list(sprite_vars[player]['pos'])
                v[0] += sprite_vars[player]['speed']
                sprite_vars[player]['pos'] = tuple(v)
            if player_move_dir == 3:
                v = list(sprite_vars[player]['pos'])
                v[1] += sprite_vars[player]['speed']
                sprite_vars[player]['pos'] = tuple(v)
            if player_move_dir == 4:
                v = list(sprite_vars[player]['pos'])
                v[0] -= sprite_vars[player]['speed']
                sprite_vars[player]['pos'] = tuple(v)

        for ghost_ in [ghost1, ghost2, ghost3]:
            if player.get_rect(topleft=sprite_vars[player]['pos']).colliderect(ghost_.get_rect(topleft=sprite_vars[ghost_]['pos'])):
                if pellet_enabled == True:
                    sprite_vars[ghost_] = init_sprite_vars[ghost_]
                else:
                    sprite_vars[player] = init_sprite_vars[player]
            ghost_move(ghost_)

        for pellet_ in pellets:
            screen.blit(pellet, pellet_)
            if player.get_rect(topleft=sprite_vars[player]['pos']).colliderect(pellet.get_rect(topleft=pellet_)):
                pellets.remove(pellet_)

        if sprite_vars[player]['pos'] == (20, 360):
            sprite_vars[player]['pos'] = (665, 360)
        if sprite_vars[player]['pos'] == (670, 360):
            sprite_vars[player]['pos'] = (20, 360)

        if pellets == []:
            level += 1
            pygame.display.set_caption('P.A.C.M.A.N - Level ' + str(level))
            pellets = [(40, 40), (80, 40), (120, 40), (160, 40), (200, 40), (240, 40), (280, 40), (320, 40), (400, 40), (440, 40), (480, 40), (520, 40), (560, 40), (600, 40), (640, 40), (680, 40),
                       (40, 90), (160, 90), (320, 90), (400, 90), (560, 90), (680, 90),
                       (40, 140), (80, 140), (120, 140), (160, 140), (200, 140), (240, 140), (280, 140), (320, 140), (400, 140), (440, 140), (480, 140), (520, 140), (560, 140), (600, 140), (640, 140), (680, 140),
                       (40, 220), (80, 220), (120, 220), (160, 220), (240, 220), (280, 220), (320, 220), (400, 220), (440, 220), (480, 220), (560, 220), (600, 220), (640, 220), (680, 220)]

        clock.tick(60)
        pygame.display.flip()

except Exception as e:
    print(e)
    pass
