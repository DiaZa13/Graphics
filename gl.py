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


# COLORS
BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)
testing = color(0.2, 1, 1)


# Creación de clase para hacer renderizar
class Render(object):
    def __init__(self, width, height):  # constructor
        # Las variables se crean dentro del constructor
        self.draw_color = WHITE
        self.clear_color = BLACK
        # Window size
        self.width = width
        self.height = height
        # Viewport size
        # self.vw_width = vw_width
        # self.vw_height = vw_height
        # self.vw_x = x
        # self.vw_y = y
        # Create a new window
        self.createWindow()


    # -------- CLEAR
    # Define el color con el que se va a limpiar la pantalla
    def clearColor(self, r, g, b):
        self.clear_color = color(r, g, b)

    # Limpiar pixeles de la pantalla (ponerlos todos en blanco o negro)
    def clear(self):
        # Estructura para almacenar los pixeles de 2D para limpiar pantalla
        self.pixels = [[self.clear_color for y in range(self.height)] for x in range(self.width)]


    # Creación de la ventana
    def createWindow(self):
        self.clear()

    # Viewport
    def createViewport(self, width, height, x, y):
        self.vw_width = width
        self.vw_height = height
        self.vw_x = x
        self.vw_y = y
        for a in range(x, (self.vw_width + x + 1)):
            for b in range(y, (self.vw_height + y + 1)):
                self.pixels[a][b] = self.draw_color


    # --------- DRAW
    def drawColor(self, r, g, b):
        self.draw_color = color(r, g, b)

    def drawPoint(self, x, y):
        relative_x = self.vw_x + ((self.vw_width / 2) * (x + 1))
        relative_y = self.vw_y + ((self.vw_height / 2) * (y + 1))
        self.pixels[relative_x][relative_y] = self.draw_color

    '''
    Creación de bitmap
    @:arg filename: nombre del documento .bmp
    '''

    def end(self, filename):
        with open(filename, 'wb') as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            # 14 bytes del header + 40 InfoHeader + color table → ancho * altura * 3 (r,g,b) de cada uno
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            # 4 bytes reservados vacíos
            file.write(dword(0))
            file.write(dword(14 + 40))
            # InfoHeader
            # Tamaño de infoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
