import pygame, itertools as it, sys
from sim import Simulation
import numpy as np
from settings import settings

class App:
    def __init__(self):
        self.sim = Simulation()

        print('Initializing pygame...')
        pygame.init()

        print('Setting fonts...')
        self.fonts = {
            "small font": pygame.font.Font(None, 25)
            }

        self.screen_size = settings['screen_size']
        self.init_images()
        self.init_screen()

        self.sim.draw(self.images)

        self.main_loop()

        self.cleanAndExit()

    def init_images(self):
        print('Loading images...')
        self.images = {}
        self.images['star0'] = pygame.image.load('img/star0.png')
        self.images['star0'].set_colorkey((0,0,0))
        self.images['star1'] = pygame.image.load('img/star0.png')
        self.images['star1'].set_colorkey((0,0,0))

        self.images['star0yellow'] = self.colored_copy(self.images['star0'], (0, 255, 255, 0))

    def init_screen(self):
        logo = pygame.image.load("img/logo.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Stars")

        self.screen = pygame.display.set_mode(self.screen_size)

        self.screen.fill((10,10,10))

    def colored_copy(self, surface, new_color):
        '''This replaces only the white color. For usage in star coloring.'''
        newsurf = surface.copy()
        newarr = pygame.PixelArray(newsurf)
        newarr.replace((255, 255, 255), new_color, weights=(1,1,1))
        del newarr
        return newsurf

    def main_loop(self):
        running = True

        space_size = settings['space_size']

        camera_position = [
                space_size[0]/2 - self.screen_size[0]/2,
                space_size[1]/2 - self.screen_size[0]/2
                ]
        cam_speed = settings.get('camera_speed', 1)
        movement = None

        while running:
            self.screen.fill((10, 10, 10))
            self.sim.tick()
            camera_position = list(self.sim.draw_on(self.screen, offset=camera_position))

            self.draw_position(self.screen, np.array(pygame.mouse.get_pos())+ np.array(camera_position))

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
                        self.sim.generate_stars()
                        self.sim.generate_nebulas()
                        self.sim.draw(self.images)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_w or \
                        event.key == pygame.K_d or event.key == pygame.K_s:
                            movement = None

            pygame.display.flip()

    def draw_position(self, surface, position):
        indicator = 'x: {}, y: {}'.format(*position)
        text_surf = self.fonts['small font'].render(
                indicator, True, (0, 0, 0),
                (240, 240, 240, 0.5)
                )
        surface.blit(text_surf, (0, 0))

    def cleanAndExit(self):
        pygame.quit()
        sys.exit()

if __name__=="__main__":
    app = App()
