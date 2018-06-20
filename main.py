import pygame, itertools as it, sys
from stars import generate_stars

def cleanAndExit():
    pygame.quit()
    sys.exit()

def draw_stars(images, stars, surface, offset=(0, 0)):
    for star in stars:
        surface.blit(images['star'+ str(star.size)],
                (star.position[0] - offset[0], star.position[1] - offset[1]))

def init_screen(screen_size):
    pygame.init()
    logo = pygame.image.load("img/logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Stars")

    screen = pygame.display.set_mode(screen_size)

    screen.fill((10,10,10))
    return screen

def init(screen_size):
    screen = init_screen(screen_size)

    images = {}
    images['star0'] = pygame.image.load('img/star0.png')
    images['star0'].set_colorkey((0,0,0))
    images['star1'] = pygame.image.load('img/star0.png')
    images['star1'].set_colorkey((0,0,0))

    stars = generate_stars(screen_size)
    draw_stars(images, stars, screen)

    return screen, images, stars

def main_loop(screen, images, stars):
    running = True

    camera_position = [0, 0]
    cam_speed = 5

    while running:
        screen.fill((10, 10, 10))
        draw_stars(images, stars, screen, offset=camera_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_a:
                    camera_position[0] -= cam_speed
                if event.key == pygame.K_s:
                    camera_position[1] += cam_speed
                if event.key == pygame.K_d:
                    camera_position[0] += cam_speed
                if event.key == pygame.K_w:
                    camera_position[1] -= cam_speed

        pygame.display.flip()


def main(screen_size=(700,500)):
    screen, images, stars = init(screen_size)

    main_loop(screen, images, stars)

    cleanAndExit()

if __name__=="__main__":
    main()
