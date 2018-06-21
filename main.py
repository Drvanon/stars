import pygame, itertools as it, sys
from stars import generate_stars

def cleanAndExit():
    pygame.quit()
    sys.exit()

def draw_stars(images, stars, surface, offset=(0, 0)):
    for star in stars:
        if star.mass == 1:
            surface.blit(images['star0'],
                (star.position[0] - offset[0], star.position[1] - offset[1]))
        if star.mass == 0:
            surface.blit(images['star0yellow'],
                (star.position[0] - offset[0], star.position[1] - offset[1]))


def init_screen(screen_size):
    pygame.init()
    logo = pygame.image.load("img/logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Stars")

    screen = pygame.display.set_mode(screen_size)

    screen.fill((10,10,10))
    return screen

def colored_copy(surface, new_color):
    '''This replaces only the white color. For usage in star coloring.'''
    newsurf = surface.copy()
    newarr = pygame.PixelArray(newsurf)
    newarr.replace((255, 255, 255), new_color, weights=(1,1,1))
    del newarr
    return newsurf

def init(screen_size):
    screen = init_screen(screen_size)

    images = {}
    images['star0'] = pygame.image.load('img/star0.png')
    images['star0'].set_colorkey((0,0,0))
    images['star1'] = pygame.image.load('img/star0.png')
    images['star1'].set_colorkey((0,0,0))

    images['star0yellow'] = colored_copy(images['star0'], (0, 255, 255, 0))

    stars = generate_stars(screen_size)
    draw_stars(images, stars, screen)

    return screen, images, stars

def main_loop(screen, images, stars, screen_size):
    running = True

    camera_position = [0, 0]
    cam_speed = 1
    movement = None

    while running:
        screen.fill((10, 10, 10))
        draw_stars(images, stars, screen, offset=camera_position)

        if movement == 'left':
            camera_position[0] -= cam_speed
        if movement == 'right':
            camera_position[0] += cam_speed
        if movement == 'up':
            camera_position[1] -= cam_speed
        if movement == 'down':
            camera_position[1] += cam_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_a:
                    movement = 'left'
                if event.key == pygame.K_s:
                    movement = 'down'
                if event.key == pygame.K_d:
                    movement = 'right'
                if event.key == pygame.K_w:
                    movement = 'up'
                if event.key == pygame.K_r:
                    stars = generate_stars(screen_size)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_w or \
                    event.key == pygame.K_d or event.key == pygame.K_s:
                        movement = None

        pygame.display.flip()


def main(screen_size=(700,500)):
    screen, images, stars = init(screen_size)

    main_loop(screen, images, stars, screen_size)

    cleanAndExit()

if __name__=="__main__":
    main()
