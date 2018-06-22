import numpy as np
from helper_functions import distance, randround

class Nebula:
    def __init__(self, sim):
        num_centers = randround(
                sim.settings['sim'].get('avg_nebula_centers', 10),
                sim.settings['sim']
        self.cloud_centers = np.rand(, 2)
