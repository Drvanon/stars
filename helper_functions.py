def randround(around, sigma):
    return randint(around - sigma, around + sigma)

def distance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1]-pos2[1])**2)


