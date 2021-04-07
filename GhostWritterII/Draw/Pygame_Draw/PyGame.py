import pygame

pygame.init()


def screen(width, height):
    size = [height, width]
    r_screen = pygame.display.set_mode(size)
    r_screen.fill((0, 0, 0))
    pygame.display.set_caption('pygame')

    return r_screen


def clear(width, height):

    size = [height, width]
    r_screen = pygame.display.set_mode(size)
    r_screen.fill((0, 0, 0))
    pygame.display.update()


    return r_screen


def draw_line(r_screen, x1, y1, x2, y2, color_of_drawing, thickness):
    pygame.draw.line(r_screen, color_of_drawing, (x1, y1), (x2, y2), thickness)

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

            quit()

    return r_screen
