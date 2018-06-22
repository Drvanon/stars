import numpy as np
from helper_functions import distance, constrain, constrain_position
import pygame
from collections import namedtuple

class Cloud(namedtuple('Cloud', ['center', 'radius'])):
    pass

class Nebula:
    def __init__(self, sim):
        self.top_left = np.random.rand(2) * sim.settings['space_size']

        num_centers = np.random.randn()
        num_centers *= sim.settings['nebulas'].get('avg_nebula_centers', 10)
        num_centers += sim.settings['nebulas'].get('centers_sigma', 5)
        num_centers = abs(int(np.round(num_centers)))

        centers = np.random.randn(num_centers, 2)
        centers *= sim.settings['nebulas'].get('cloud_dispersion', 200)
        centers += 2*sim.settings['nebulas'].get('cloud_dispersion', 200)

        radii = np.random.randn(num_centers)
        radii *= int(sim.settings['nebulas'].get('avg_center_radius', 10))
        radii += sim.settings['nebulas'].get('center_radius_sigma', 5),

        self.clouds = [Cloud(center, radius) for center, radius in zip(centers, radii)]
        self.width = np.rint(max(self.clouds, key=lambda c: c.center[0] + c.radius)[0][0]).astype(np.int)
        self.height = np.rint(max(self.clouds, key=lambda c: c.center[1] + c.radius)[0][1]).astype(np.int)

        self.top_left = constrain_position(
                self.top_left, (0, 0),
                sim.settings['screen_size'] - np.array((self.width, self.height))
            )

        self.color = (66, 134, 244)

        self.surface = pygame.Surface((self.width, self.height))
        for i in range(self.width):
            for j in range(self.height):
                strength = sum([ 1/distance((i, j), cc.center/cc.radius)**2 for cc in self.clouds ])
                strength = constrain(strength, 0, 1)
                res_color = np.around(strength*np.array([155,155,155]).astype(np.int))
                res_color = constrain_position(res_color, (10,10,10), (155, 155, 155))
                self.surface.set_at((i, j), res_color)
        self.surface.set_colorkey((0,0,0))

        for center in self.clouds:
            print(center)

def generate_nebulas(sim, avg_nebulas, sigma_nebulas):
    nebulas = []
    num_nebulas = np.random.randn()
    num_nebulas *= sigma_nebulas
    num_nebulas += avg_nebulas
    num_nebulas = abs(int(np.round(num_nebulas)))

    for i in range(num_nebulas):
        nebulas.append(Nebula(sim))

    return nebulas
