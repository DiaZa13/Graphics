# Funciones para uso general
# Interpreta bytes y los empaca como datos binarios
import struct


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


def _color(r, g, b):
    # Comúnmente la tarjeta de video en colores acepta valor de 0 a 1
    # Y para convertirlo en byte se multiplica por 255
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

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


# # Por si se usan los vértices puros sin transformación
# vert0 = model.vertices[face[0][0] - 1]
# vert1 = model.vertices[face[1][0] - 1]
# vert2 = model.vertices[face[2][0] - 1]
#
# # Coordenadas de textura
# vt0 = model.textures[face[0][1] - 1]
# vt1 = model.textures[face[1][1] - 1]
# vt2 = model.textures[face[2][1] - 1]
#
# # Transformación de vértices por la matriz del modelo
# _a = self.transform(vert0, modelMatrix)
# _b = self.transform(vert1, modelMatrix)
# _c = self.transform(vert2, modelMatrix)
# # En caso de que tenga 4 vertices
# if vertex_count == 4:
#     vert3 = model.vertices[face[3][0] - 1]
#     vt3 = model.textures[face[3][1] - 1]
#     _d = self.transform(vert3, modelMatrix)