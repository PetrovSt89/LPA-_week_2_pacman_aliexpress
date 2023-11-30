import random
import time

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


class Chest_2(GameObject):
    sprite_filename = "chest_2"

class Chest_OLD(GameObject):
    sprite_filename = "chest_old"


LEFT_X = 40
RIGHT_X = 560
HIGHT_Y = 40
LOW_Y = 400

HEALTH = 10


def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    """функция вырисовки стен по периметру"""
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


def calculate_lab_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    """функция вырисовки лабиринта"""
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height

    lab_coordinates = []

    random_hole = 4
    random_lab = 3
    for block_num in range(2,horizontal_wall_blocks_amount -2):
        if block_num%random_hole!=0:
            lab_coordinates.extend([
                (block_num * wall_block_width, wall_block_height*random_lab),
                (block_num * wall_block_width, wall_block_height*random_lab*2),
                (block_num * wall_block_width, wall_block_height*random_lab*3),
            ])
    for block_num in range(2, vertical_wall_blocks_amount - 2):
        if block_num%random_hole!=0:
            lab_coordinates.extend([
                (wall_block_width*random_lab, block_num * wall_block_height),
                (wall_block_width*random_lab*2, block_num * wall_block_height),
                (wall_block_width*random_lab*3, block_num * wall_block_height),
                (wall_block_width*random_lab*4, block_num * wall_block_height)
            ])
    
    return lab_coordinates


def compose_context(screen):
    """функция обЪявления обЪектов"""
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    lab_coordinates = calculate_lab_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    lab_1 = [(120,40), (80, 80), (80, 200), (80, 320), (80, 360),(160, 120), (160, 240), (160, 280),
             (120, 360), (160, 360), (200, 80), (240, 160), (200, 200), (320, 40), (360, 40),(240, 200), (240, 240),
             (280, 320), (320, 320), (240, 400), (360, 360), (440, 400), (560, 200), (320, 200), (520, 360),
             (400, 120), (400, 160), (400, 280), (480, 80), (480, 240), (480, 280), (520, 80), (360, 120)]
            
    all_coordinates = walls_coordinates + random.choice([lab_1, lab_coordinates])
    return {
        "player": Player(LEFT_X, LOW_Y),
        "walls": Group(*[Wall(x, y) for (x, y) in all_coordinates]),
        "score_name": "health: ",
        "score": HEALTH,
        "score_2_name": "points: ",
        "score_2": 0,
        "chest": Chest(LEFT_X, HIGHT_Y),
        "chest_2": Chest_2(RIGHT_X, HIGHT_Y),
        "chest_old": Chest_OLD(RIGHT_X, LOW_Y),
        "all_coordinates": all_coordinates,
    }


def draw_whole_screen(screen, context):
    """функция вырисовки обЪектов"""
    screen.fill("grey")
    context["player"].draw(screen)
    context["walls"].draw(screen)
    context["chest"].draw(screen)
    context["chest_2"].draw(screen)
    context["chest_old"].draw(screen)
    Text(str(context["score_name"]), (10, 10)).draw(screen)
    Text(str(context["score"]), (90, 10)).draw(screen)
    Text(str(context["score_2_name"]), (130, 10)).draw(screen)
    Text(str(context["score_2"]), (210, 10)).draw(screen)


def move_chest(chest, player):
    """функция приближения ящика к игроку"""
    chest_speed = random.randint(1,7)
    old_chest_x, old_chest_y, width_chest, height_chest = chest.rect
    old_player_x, old_player_y, width_player, height_player = player.rect
    
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



def move_player(context):
    """функция движения игрока клавишами"""
    player_speed = 5
    keys = pygame.key.get_pressed()

    pressed_dict = {
        pygame.K_w: (0, -1 * player_speed),
        pygame.K_s: (0, player_speed),
        pygame.K_a: (-1 * player_speed, 0),
        pygame.K_d: (player_speed, 0)
    }

    for k,v in pressed_dict.items():
        if keys[k]:
            context["player"].rect = context["player"].rect.move(v[0], v[1])


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    running = True
    lis_title = pygame.image.load("lis_title.png")
    lis_game_over = pygame.image.load("resources/game_over.png")
    
    screen.blit(pygame.transform.scale(lis_title, [640,480]), [10, 10])
    pygame.display.flip()
    time.sleep(2)

    # обЪявляем обЪекты
    context = compose_context(screen)



    # кнопка выключения
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # включаем вырисовку
        draw_whole_screen(screen, context)
        pygame.display.flip()

        # сохраним старый ход игрока и будем двигать игрока
        old_player_topleft = context["player"].rect.topleft
        move_player(context)

        # сохраним старый ход ящиков
        old_chest_topleft = context["chest"].rect.topleft
        old_chest_2_topleft = context["chest_2"].rect.topleft

        
        # двигаем ящики
        for chest in (context["chest"], context["chest_2"]):
            move_chest(chest, context["player"])


        # проверяем столкновение обЪектов со стеной
        for obj in (
            (context["player"], old_player_topleft),
            (context["chest"], old_chest_topleft),
            (context["chest_2"], old_chest_2_topleft),
            ):
            if spritecollide(obj[0], context["walls"], dokill=False):
                obj[0].rect.topleft = obj[1]
        
        # проверяем столкновение игрока с ящиками
        for chest in (context["chest"], context["chest_2"]):
            if context["player"].is_collided_with(chest):
                context["score"] -= 1
                chest.rect.topleft = random.choice(
                    [(LEFT_X, HIGHT_Y), (RIGHT_X, HIGHT_Y), (LEFT_X, LOW_Y)]
                    )
                
        # если здоровье закончилось, конец игры
        if context["score"] == 0:
            screen.blit(pygame.transform.scale(lis_game_over, [640,480]), [10, 10])
            pygame.display.flip()
            time.sleep(3)
            running = False
        
        # проверяем столкновение ящиков между собой
        if context["chest"].is_collided_with(context["chest_2"]):
                context["score"] += 1
                context["chest"].rect.topleft = random.choice(
                    [(LEFT_X, HIGHT_Y), (RIGHT_X, HIGHT_Y), (LEFT_X, LOW_Y)]
                    )

        if context["player"].is_collided_with(context["chest_old"]):
            context["score_2"] += 1
            while True:
                position = Wall.width * random.randint(2, 13),Wall.height * random.randint(2, 9)
                if position not in context["all_coordinates"]:
                    context["chest_old"].rect.topleft = (
                        position[0],
                        position[1],
                        )
                    break
        
        clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
