from settings import settings
from nebulas import Nebula, generate_nebulas
from stars import Star, generate_stars
import pygame
from helper_functions import constrain_position

class Simulation:
    def __init__(self):
        self.time = settings['sim']['time'].get('start', 0)

        self.generate_stars()
        self.generate_nebulas()

        self.surf = pygame.Surface(settings['space_size'])
        self.surf.set_colorkey((0,0,0))


    def generate_stars(self):
        print('Generating stars')
        self.stars = []
        self.stars = generate_stars(
            settings.get("space_size", (700, 500)),
            settings.get("avg_groups", 10),
            settings.get("groups_sigma", 3),
            settings.get("avg_group_size", 10),
            settings.get("group_size_sigma", 3),
            settings.get("position_sigma", 50)
            )

    def generate_nebulas(self):
        self.nebulas = generate_nebulas(settings)

    def draw_stars(self, images, surface, offset):
        for star in self.stars:
            if star.mass == 1:
                surface.blit(images['star0'],
                    (star.position[0] - offset[0], star.position[1] - offset[1]))
            if star.mass == 0:
                surface.blit(images['star0yellow'],
                    (star.position[0] - offset[0], star.position[1] - offset[1]))

    def draw_nebulas(self, offset):
        for nebula in self.nebulas:
            self.surf.blit(nebula.surface, nebula.top_left)

    def draw(self, images):
        center_offset = (
                -settings['space_size'][0]/2,
                -settings['space_size'][1]/2
            )
        self.draw_stars(images, self.surf, (0, 0))
        self.draw_nebulas(center_offset)

    def draw_on(self, surface, offset=(0,0)):
        offset = constrain_position(
                offset, (0, 0),
                (
                    self.surf.get_width() - surface.get_width(),
                    self.surf.get_height() - surface.get_height())
                )
        new_surf = self.surf.subsurface(offset, (surface.get_width(), surface.get_height()))
        surface.blit(new_surf, (0,0))
        return offset

    def tick(self):
        self.time += settings['sim']['time'].get('time_increment', 1)


if __name__=="__main__":
    sim = Simulation()
