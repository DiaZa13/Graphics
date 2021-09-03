# Figuras para las intersecciones
import libs.zmath as zm
import libs.zutils as zu
import numpy as np

class Materials(object):
    def __init__(self, diffuse=zu._color(0, 0, 0)):
        # diffuse = color de la superficie
        self.diffuse = diffuse

class Intersect(object):
    def __init__(self, distance):
        # distance = distancia a la que hace contacto
        self.distance = distance

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def rayIntersect(self, origin, direction):
        # P = O + t * D
        # O = origen
        # t = distancia recorrida
        # D = dirección del rayo
        L = zm.subtract(self.center, origin)
        # Tca = distancia perpendicular del origen al centro
        tca = zm.dot(L, direction)
        # Magnitud de L
        #Implementar calculo de magnitud
        l = np.linalg.norm(L)

        d = (l ** 2 - tca ** 2) ** 0.5
        # d = punto perpendicular más cercano al centro de la esfera

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            if t1 < 0:
                return None
            else:
                t0 = t1
        # La cámara está dentro de la esfera (están en la misma posición)


        # La esfera está detrás de la cámara
        return Intersect(distance=t0)
