# Funciones para uso general
# Interpreta bytes y los empaca como datos binarios
from collections import namedtuple
import struct

import numpy as np

from libs import zmath as zm

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

# Permite asegurar que únicamente se utilize un byte
def char(c):
    # 1 byte, ya que el char de Python ocupa 4 bytes
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def colors(r, g, b):
    # Comúnmente la tarjeta de video en colores acepta valor de 0 a 1
    # Y para convertirlo en byte se multiplica por 255
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

#Colores básicos
WHITE = colors(1, 1, 1)
BLACK = colors(0, 0, 0)
RED = colors(1, 0, 0)


def baryCoords(A, B, C, P):
    # u es para A, v es para B, w es para C
    # ABC
    ABC = ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y))
    # PCB/ABC
    try:
        u = ((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) / ABC
        v = ((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) / ABC
        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

def reflection(normal, directional_light):
    # R = 2 * (normal • light) * normal - light
    a = 2 * zm.dot(normal, directional_light)
    reflect = np.multiply(a, normal)
    reflect = zm.subtract(reflect, directional_light)
    reflect = zm.normalize(reflect)

    return reflect
