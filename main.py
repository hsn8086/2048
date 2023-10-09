import copy
import itertools
import random
import time
from pathlib import Path

import pygame
from pygame import Surface

from util import Block, AnimUpdater

d_rect = {}


def bg_update(screen):
    screen.fill((255, 255, 255))
    for x, y in itertools.product(range(4), range(4)):
        pygame.draw.rect(screen, (238, 238, 238), (x * 200 + 20, y * 200 + 20, 180, 180), 0, border_radius=5)


def event_process_main_logic(event) -> bool:
    if event.type == pygame.KEYDOWN:
        # set the forward and reverse order and direction of movement
        v_x, v_y = 0, 0
        r_x = range(4)
        r_y = range(4)
        if event.key == pygame.K_DOWN:
            v_y = 1
            r_y = range(3, -1, -1)
        elif event.key == pygame.K_RIGHT:
            v_x = 1
            r_x = range(3, -1, -1)
        elif event.key == pygame.K_UP:
            v_y = -1
        elif event.key == pygame.K_LEFT:
            v_x = -1
        moved = 0
        for x, y in itertools.product(r_x, r_y):
            if (x, y) in d_rect:
                while True:
                    # get the next position
                    x1, y1 = x + v_x, y + v_y

                    # check if the next position is out of bounds
                    if x1 < 0 or x1 > 3 or y1 < 0 or y1 > 3:
                        break

                    # check if the next position is empty
                    if (x1, y1) in d_rect:
                        # if the next position is not empty, check if the number is the same
                        if d_rect[x1, y1].num == d_rect[x, y].num:
                            # if the number is the same, merge the two blocks
                            d_rect[x, y].num += 1
                            d_rect.pop((x1, y1))
                        else:
                            break

                    # move the block to the next position
                    d_rect[x1, y1] = d_rect[x, y]
                    d_rect.pop((x, y))

                    # update the position of the block
                    d_rect[x1, y1].move_to(x1, y1)
                    x, y = x1, y1
                    moved += 1
        if len(d_rect) == 16:
            # check if the game is over

            return False
        if moved > 0 or len(d_rect) == 0:
            # add a new block
            block = Block(d_rect)
            d_rect[block.x, block.y] = block

    return True


def event_process(event) -> bool:
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    return event_process_main_logic(event)


def new_game():
    for i in copy.copy(d_rect):
        del d_rect[i]

    bg_update(screen)

    pygame.display.update()
    fcc_lock = pygame.time.Clock()
    while True:
        if not min([event_process(event) for event in pygame.event.get()] + [True]):
            text = font.render('Game Over', True, (0, 0, 0))
            tx, ty = text.get_size()
            size_x, size_y = size
            screen.blit(text, (size_x // 2 - tx // 2, size_y // 2 - ty // 2))
            pygame.display.update()
            break
        # update and get the animation list
        anim_list: list[AnimUpdater] = [block.update(screen) for block in d_rect.values()]

        # update the animation
        b = False
        while anim_list:
            bg_update(screen)

            if len(list(filter(lambda x: x.update() <= 0, anim_list))) > 0:
                break

            pygame.display.update()
            fcc_lock.tick(60)


if __name__ == '__main__':
    pygame.init()
    font = pygame.font.Font((Path('assets') / 'font' / 'unifont-15.1.02.otf'), 100)
    size = (800, 800)
    screen: Surface = pygame.display.set_mode(size=size)
    pygame.display.set_caption("2048")
    while True:
        new_game()
        time.sleep(3)
        pygame.event.get()
