import pygame
import random

from pygame.sprite import spritecollide

from compose_context import Wall
from const import const
from move import move_chest, move_player
from text import Text
from utils import headpiece


def exit_button() -> None:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def draw_whole_screen(screen, context) -> None:
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


def not_health(context, screen) -> bool:
    if context["score"] == 0:
        headpiece(screen=screen, path_pic="resources/game_over.png")
        return False
    else:
        return True


def touch_walls(context, objects) -> None:
    for obj in objects:
        if spritecollide(obj[0], context["walls"], dokill=False):
            obj[0].rect.topleft = obj[1]


def touch_objects(context, obj_one, obj_two) -> None:
    for chest in obj_two:
        if obj_one.is_collided_with(chest):
            if obj_one == context["player"]:
                context["score"] -= 1
            elif obj_one == context["chest"]:
                context["score"] += 1
            chest.rect.topleft = random.choice(
                [(const.LEFT_X, const.HIGHT_Y),
                    (const.RIGHT_X, const.HIGHT_Y),
                    (const.LEFT_X, const.LOW_Y)]
                    )

def collect_chest(context, obj_one, obj_two) -> None:
    if obj_one.is_collided_with(obj_two):
        context["score_2"] += 1
        while True:
            position = Wall.width * random.randint(2, 13),Wall.height * random.randint(2, 9)
            if position not in context["all_coordinates"]:
                obj_two.rect.topleft = (
                    position[0],
                    position[1],
                    )
                break


def game_logic(running, screen, context, clock) -> None:
    while running:
        
        # кнопка выключения
        exit_button()

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
        touch_walls(context=context, 
                    objects=((context["player"], old_player_topleft),
                                (context["chest"], old_chest_topleft),
                                (context["chest_2"], old_chest_2_topleft),
                    ))
        
        
        # проверяем столкновение игрока с ящиками
        touch_objects(context=context, 
                      obj_one=context["player"], 
                      obj_two=(context["chest"], context["chest_2"]))
        
                
        # если здоровье закончилось, конец игры 
        running = not_health(context, screen)
        

        # столкновение ящиков между собой
        touch_objects(context=context, obj_one=context["chest"], obj_two=(context["chest_2"],))
        
        
        # собирание ящиков, попадание ящика в рандомное поле
        collect_chest(context=context, obj_one=context["player"], obj_two=context["chest_old"])
        
        
        clock.tick(60) / 1000