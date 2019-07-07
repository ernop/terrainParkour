import math

def getDistance(sign1, sign2):
    return math.sqrt(math.pow(sign1.x-sign2.x, 2) + math.pow(sign1.y-sign2.y, 2) + math.pow(sign1.z-sign2.z, 2))
