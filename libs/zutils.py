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

def color(r, g, b):
    # Comúnmente la tarjeta de video en colores acepta valor de 0 a 1
    # Y para convertirlo en byte se multiplica por 255
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


def baryCoords(A, B, C, P):
    # u es para A, v es para B, w es para C
    # ABC
    ABC = ((B.y - C.y) * (A.x - C.x)  )