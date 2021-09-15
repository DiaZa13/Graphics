# Figuras para las intersecciones
import libs.zmath as zm
from libs.zutils import V3, WHITE
import numpy as np

class DirectionalLight(object):
    def __init__(self, direction=V3(0, -1, 0), intensity=1, color=WHITE):
        self.direction = zm.normalize(direction)
        self.intensity = intensity
        self.color = color

class AmbientLight(object):
    def __init__(self, strength=0, color=WHITE):
        self.strength = strength
        self.color = color

class PointLight(object):
    # Es una luz con un punto de origen que se esparce a todas las direcciones
    # "genera" una cantidad infinita de rayos de luz en todas las direcciones
    def __init__(self, position=V3(0, 0, 0), intensity=1, color=WHITE):
        self.position = position
        self.intensity = intensity
        self.color = color


class Intersect(object):
    def __init__(self, distance, point, normal, figure):
        # distance = distancia a la que hace contacto
        self.distance = distance
        self.point = point
        self.normal = normal
        self.figure = figure


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
        # Implementar calculo de magnitud
        l = zm.hypotenuse(L)

        d = (l ** 2 - tca ** 2) ** 0.5
        # d = punto perpendicular más cercano al centro de la esfera

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        # La cámara está dentro de la esfera (están en la misma posición)
        # La esfera está detrás de la cámara
        if t0 < 0:
            if t1 < 0:
                return None
            else:
                t0 = t1

        # Intersect point
        # Agregar a mi librería la multiplicación de escalar por vector
        hit = zm.sum(origin, V3(t0 * direction[0],
                                t0 * direction[1],
                                t0 * direction[2]))
        # Normal
        normal = zm.subtract(hit, self.center)
        # Asegurar normalizar la normal
        normal = zm.normalize(normal)

        return Intersect(distance=t0, point=hit, normal=normal, figure=self)
