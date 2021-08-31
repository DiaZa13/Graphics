# Figuras para las intersecciones
import libs.zmath as zm
import numpy as np
class Sphere(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def rayIntersect(self, origin, direction):
        # P = O + t * D
        L = zm.subtract(self.center, origin)
        # Tca = distancia perpendicular del origen al centro
        tca = zm.dot(L, direction)
        # Magnitud de L
        #Implementar calculo de magnitud
        l = np.linalg(L)

        d = (l ** 2 - tca ** 2) ** 0.5
        if d > self.radius:
            return False

        return True
