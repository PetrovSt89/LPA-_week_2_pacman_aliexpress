import pygame
import time

from text import Text

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


def headpiece(screen, path_pic: str) -> None:
    """функция вырисовки заставки"""
    pic = pygame.image.load(path_pic)
    screen.blit(pygame.transform.scale(pic, [640,480]), [10, 10])
    pygame.display.flip()
    time.sleep(2)

