from random import randint, choice
from math import sqrt
import itertools as it
from helper_functions import distance, randround

class Star:
    def __init__(self, size, position):
        self.size = size
        self.position = position
        self.mass = choice([0, 1])

def generate_stars(space_size, avg_groups, groups_sigma, avg_group_size, group_size_sigma, position_sigma):
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

