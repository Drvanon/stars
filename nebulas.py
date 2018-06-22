import numpy as np
from helper_functions import distance, randround
import pygame
from collections import namedtuple

class Cloud(namedtuple('Cloud', ['center', 'radius'])):
    pass


class Nebula:
    def __init__(self, sim):
        self.top_right = np.random.rand(2) * sim.space_size

        num_centers = np.randn()
        num_centers *= sim.settings['nebulas'].get('avg_nebula_centers', 10)
        num_centers += sim.settings['nebulas'].get('centers_sigma', 5)

        centers = np.random.randn(num_centers, 2)
        centers *= sim.settings['nebulas'].get('cloud_dispersion', 20)

        radii = np.random.randn(num_centers, 1)
        radii *= sim.settings['nebulas'].get('avg_center_radius', 10)
        radii += sim.settings['nebulas'].get('center_radius_sigma', 5),

        self.clouds = [Cloud(center, radius) for center, radius in zip(centers, radii)]

    def draw(self, surface):
        # Accomodate for the size of the clouds
        x = max(self.clouds, key=lambda c: c.center[0] + c.radius)
        y = max(self.clouds, key=lambda c: c.center[1] + c.radius)
        surf = pygame.Surface((x, y))

        for i in range(10):
            for j in range(10):
                surf.set_at((i, j), (155,155,155))

        return surf
