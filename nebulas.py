import numpy as np
from helper_functions import distance, constrain, constrain_position
import pygame
from collections import namedtuple
from settings import settings
import timeit

class Cloud:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return '<Cloud at ({}, {})>'.format(*self.center)

class Nebula:
    def __init__(self, settings, centers=[], radii=[]):
        self.top_left = np.random.rand(2) * settings['space_size']

        self.color = (66, 134, 244)

        if not centers and not radii:
            centers, radii = self.generate_random_values(settings)

        self.clouds = [Cloud(center, radius) for center, radius in zip(centers, radii)]

        # Bring Clouds to topleft and offset by 20
        bounding_rect = self.get_bounding_rect()
        print('bounding rect:', bounding_rect)
        for cloud in self.clouds:
            cloud.center[0] -= bounding_rect[0]
            cloud.center[1] -= bounding_rect[1]
            cloud.center += (20, 20)

        print('-'*13)
        print('New clouds:')
        for cloud in self.clouds:
            print(cloud.center)
        print('-'*13)

        print('Bounding rect 2: ', bounding_rect)
        self.width, self.height = bounding_rect[2:]
        self.width += 40
        self.height += 40
        print('width: ', self.width, 'height', self.height)

        self.top_left = constrain_position(
            self.top_left, (0, 0),
            settings['screen_size'] - np.array((self.width, self.height))
        )

        self.surface = pygame.Surface((self.width, self.height))
        self.generate_surface()
        self.surface.set_colorkey((0,0,0))

        self.give_red_border()

        for cloud in self.clouds:
            print('Generated cloud at rel({}, {})'.format(*cloud.center))

    def generate_surface(self):
        for i in range(self.width):
            for j in range(self.height):
                #strength = sum([ 1/distance((i, j), cc.center/cc.radius)**2 for cc in self.clouds ])
                #strength = constrain(strength, 0, 1)
                #res_color = np.around(strength*np.array([155,155,155]).astype(np.int))
                #res_color = constrain_position(res_color, (10,10,10), (155, 155, 155))
                #self.surface.set_at((i, j), res_color)
                brightness = sum([1/np.linalg.norm(np.array([i,j]) - cloud.center) for cloud in self.clouds])
                brightness = constrain(brightness, 0, 1)
                self.surface.set_at((i, j), (0, brightness*255, 0))

    def give_red_border(self):
        for i in range(self.width):
            self.surface.set_at((i, 0), (255,0,0))
            self.surface.set_at((i, self.height-1), (255,0,0))
        for i in range(self.height):
            self.surface.set_at((0, i), (255,0,0))
            self.surface.set_at((self.width-1, i), (255,0,0))

    def generate_random_values(self, settings):
        num_centers = np.random.randn()
        num_centers *= settings['nebulas'].get('avg_nebula_centers', 10)
        num_centers += settings['nebulas'].get('centers_sigma', 5)
        num_centers = abs(int(np.round(num_centers)))
        num_centers = constrain(num_centers, 1, 100000)

        centers = np.random.randn(num_centers, 2)
        centers *= settings['nebulas'].get('cloud_dispersion', 200)
        centers += .5*settings['nebulas'].get('cloud_dispersion', 200)

        radii = np.random.randn(num_centers)
        radii *= int(settings['nebulas'].get('avg_center_radius', 10))
        radii += settings['nebulas'].get('center_radius_sigma', 5),

        print('---------')
        print('Initial centers:')
        for center in centers:
            print(center)
        print('---------')

        return centers, radii

    def get_bounding_rect(self):
        min_x = np.rint(min(self.clouds, key=lambda c: c.center[0]).center[0]).astype(np.int)
        min_y = np.rint(min(self.clouds, key=lambda c: c.center[1]).center[1]).astype(np.int)
        max_x = np.rint(max(self.clouds, key=lambda c: c.center[0]).center[0]).astype(np.int)
        max_y = np.rint(max(self.clouds, key=lambda c: c.center[1]).center[1]).astype(np.int)
        return (min_x, min_y, max_x - min_x, max_y - min_y)

def generate_nebulas(settings):
    avg_nebulas = settings['nebulas'].get('avg_nebulas', 10)
    sigma_nebulas = settings['nebulas'].get('sigma_nebulas', 10)
    nebulas = []
    num_nebulas = np.random.randn()
    num_nebulas *= sigma_nebulas
    num_nebulas += avg_nebulas
    num_nebulas = abs(int(np.round(num_nebulas)))

    for i in range(num_nebulas):
        nebulas.append(Nebula(settings))

    return nebulas
