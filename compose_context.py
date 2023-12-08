from typing import Any

from const import const
from game_object import GameObject
from lab import lab_1

from pygame.sprite import Group

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


def calculate_walls_coordinates(screen_width, screen_height,
                                wall_block_width, wall_block_height) -> list[tuple[int]]:
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


def compose_context(screen) -> dict[str,Any]:
    """функция обЪявления обЪектов"""
    walls_coordinates = calculate_walls_coordinates(screen.get_width(),
                                                    screen.get_height(),
                                                    Wall.width, 
                                                    Wall.height)
    
    all_coordinates = walls_coordinates + lab_1
    return {
        "player": Player(const.LEFT_X, const.LOW_Y),
        "walls": Group(*[Wall(x, y) for (x, y) in all_coordinates]),
        "score_name": "health: ",
        "score": const.HEALTH,
        "score_2_name": "points: ",
        "score_2": 0,
        "chest": Chest(const.LEFT_X, const.HIGHT_Y),
        "chest_2": Chest_2(const.RIGHT_X, const.HIGHT_Y),
        "chest_old": Chest_OLD(const.RIGHT_X, const.LOW_Y),
        "all_coordinates": all_coordinates,
    }