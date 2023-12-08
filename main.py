import pygame

from utils import headpiece


from compose_context import compose_context
from game_object import GameObject
from game_logic import game_logic


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    running = True

    headpiece(screen=screen, path_pic="resources/lis_title.png")    
    
    
    # обЪявляем обЪекты
    context = compose_context(screen)

    game_logic(running=running, screen=screen, context=context, clock=clock)

    pygame.quit()


if __name__ == "__main__":
    main()
