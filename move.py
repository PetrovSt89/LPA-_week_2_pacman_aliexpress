import pygame
import random


def move_chest(chest, player) -> None:
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


def move_player(context) -> None:
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