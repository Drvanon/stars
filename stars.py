import pygame, sys, collections, itertools as it
from random import randint
from math import sqrt

Star = collections.namedtuple('Star', ['size', 'position', 'spec_type'])

def randround(around, sigma):
    return randint(around - sigma, around + sigma)

def distance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1]-pos2[1])**2)

def generate_stars(space_size, avg_groups=10, groups_sigma=3, avg_group_size=10, group_size_sigma=3, position_sigma=50):
    stars = []
    groups = []

    # generate groups at random locations
    for i in range(randround(avg_groups, groups_sigma)):
        group_center = (randint(0, space_size[0]), randint(0, space_size[1]))
        group = []

        print('Generating star group at ({}, {})'.format(*group_center))

        for i in range(randround(avg_group_size, group_size_sigma)):
            found_star = False

            while not found_star:
                new_x_pos = randround(group_center[0], position_sigma)
                new_y_pos = randround(group_center[1], position_sigma)
                new_pos = (new_x_pos, new_y_pos)
                new_star = Star(randint(0, 1), new_pos)
                found_star = True

                # Make sure no collisions happen
                rad_of_col = 0.25 * position_sigma # Radius of collision
                for star in group:
                    if distance(new_pos, star.position) < rad_of_col:
                        found_star = False

            group.append(new_star)
        groups.append(group)

    stars += it.chain.from_iterable(groups) # Flatten groups

    print('Generated {} stars in {} groups'.format(len(stars), len(groups)))
    return stars

def draw_stars(images, stars, surface, offset=(0, 0)):
    for star in stars:
        surface.blit(images['star'+ str(star.size)],
                (star.position[0] - offset[0], star.position[1] - offset[1]))

def cleanAndExit():
    pygame.quit()
    sys.exit()

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
