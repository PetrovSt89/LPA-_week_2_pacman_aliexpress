import random

import pygame
from pygame.sprite import Group, spritecollide

from game_object import GameObject
from text import Text


class Player(GameObject):
    sprite_filename = "player"


class Wall(GameObject):
    sprite_filename = "wall"


class Chest(GameObject):
    sprite_filename = "chest"


def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height - 2

    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (block_num * wall_block_width, 0),
            (block_num * wall_block_width, screen_height - wall_block_height),
        ])
    for block_num in range(1, vertical_wall_blocks_amount + 1):
        walls_coordinates.extend([
            (0, block_num * wall_block_height),
            (screen_width - wall_block_width, block_num * wall_block_height),
        ])

    return walls_coordinates

# тут добавил рандомный лабиринт
def calculate_lab_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height - 2

    lab_coordinates = []
    random_lab = random.randint(2,4)
    for block_num in range(2,horizontal_wall_blocks_amount):
        if block_num%random_lab!=0:
            lab_coordinates.extend([
                (block_num * wall_block_width, wall_block_height*3),
                (block_num * wall_block_width, wall_block_height*6),
                (block_num * wall_block_width, wall_block_height*9),
            ])
    for block_num in range(2, vertical_wall_blocks_amount + random_lab):
        if block_num%random_lab!=0:
            lab_coordinates.extend([
                (wall_block_width*3, block_num * wall_block_height),
                (wall_block_width*6, block_num * wall_block_height),
                (wall_block_width*9, block_num * wall_block_height),
                (wall_block_width*12, block_num * wall_block_height)
            ])

    return lab_coordinates


def compose_context(screen):
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    lab_coordinates = calculate_lab_coordinates(screen.get_width() - 160, screen.get_height() - 160, Wall.width, Wall.height)
    all_coordinates = walls_coordinates + lab_coordinates
    # all_coordinates = walls_coordinates
    return {
        "player": Player(40, 400),
        "walls": Group(*[Wall(x, y) for (x, y) in all_coordinates]),
        "score": 10,
        "chest": Chest(40, 40),
        "chest_2": Chest(560, 40),
        # "chest_3": Chest(100, 340),
        # "chest_4": Chest(500, 340),
    }


def draw_whole_screen(screen, context):
    screen.fill("purple")
    context["player"].draw(screen)
    context["walls"].draw(screen)
    context["chest"].draw(screen)
    context["chest_2"].draw(screen)
    # context["chest_3"].draw(screen)
    # context["chest_4"].draw(screen)
    Text(str(context["score"]), (10, 10)).draw(screen)



def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    running = True
    player_speed = 5

    context = compose_context(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_whole_screen(screen, context)
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        old_player_topleft = context["player"].rect.topleft
        if keys[pygame.K_w]:
            context["player"].rect = context["player"].rect.move(0, -1 * player_speed)
        if keys[pygame.K_s]:
            context["player"].rect = context["player"].rect.move(0, player_speed)
        if keys[pygame.K_a]:
            context["player"].rect = context["player"].rect.move(-1 * player_speed, 0)
        if keys[pygame.K_d]:
            context["player"].rect = context["player"].rect.move(player_speed, 0)

        old_chest_topleft = context["chest"].rect.topleft
        old_chest_2_topleft = context["chest_2"].rect.topleft
        # вот тут попробую подвигать ящик
        def move_chest(chest):
            # chest_speed = 1
            chest_speed = random.randint(1,7)
            old_chest_x, old_chest_y, width_chest, height_chest = chest.rect
            old_player_x, old_player_y, width_player, height_player = context["player"].rect
            
            if old_player_x > old_chest_x:
                step_x = chest.rect.move(chest_speed, 0)
            elif old_player_x < old_chest_x:
                step_x = chest.rect.move(-1 * chest_speed, 0)
            else:
                step_x = chest.rect.move(0, 0)
            
            if old_player_y > old_chest_y:
                step_y = chest.rect.move(0, chest_speed)
            elif old_player_y < old_chest_y:
                step_y = chest.rect.move(0, -1 * chest_speed)
            else:
                step_y = chest.rect.move(0, 0)

            chest.rect = random.choice([step_x, step_y])
        
        for chest in (context["chest"], context["chest_2"]):
            move_chest(chest)
        # алгоритм движения ящика закончен


        if spritecollide(context["player"], context["walls"], dokill=False):
            context["player"].rect.topleft = old_player_topleft

        if spritecollide(context["chest"], context["walls"], dokill=False):
            context["chest"].rect.topleft = old_chest_topleft

        if spritecollide(context["chest_2"], context["walls"], dokill=False):
            context["chest_2"].rect.topleft = old_chest_2_topleft
            
        for chest in (context["chest"], context["chest_2"]):
            if context["player"].is_collided_with(chest):
                context["score"] -= 1
                chest.rect.topleft = random.choice(
                    [(40, 40), (560, 40), (40, 400)]
                    )
        
        if context["chest"].is_collided_with(context["chest_2"]):
                context["chest"].rect.topleft = random.choice(
                    [(40, 40), (560, 40), (40, 400)]
                    )

        if context["score"] == 0:

            running = False

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
