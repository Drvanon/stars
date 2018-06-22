from random import randint
from math import sqrt

def randround(around, sigma):
    return randint(around - sigma, around + sigma)

def distance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1]-pos2[1])**2)

def invert_tuple(tup):
    return (-i for i in tup)

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def constrain_position(pos, min_pos, max_pos):
    return tuple(constrain(pos[i], min_pos[i], max_pos[i]) for i in range(len(pos)))
