# Interpreta bytes y los empaca como datos binarios
import struct
from collections import namedtuple
import obj

# Creación de un tipo de variable para dibujar una línea
V2 = namedtuple('Point2', ['x', 'y'])


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
        # Default viewport
        self.viewport(self.width, self.height, 0, 0)

    # Viewport
    def viewport(self, width, height, x, y, color=None):
        self.vw_width = int(width - 1)
        self.vw_height = int(height - 1)
        self.vw_x = int(x)
        self.vw_y = int(y)

        for a in range(int(x), (self.vw_width + int(x) + 1)):
            for b in range(int(y), (self.vw_height + int(y) + 1)):
                self.pixels[a][b] = color or self.clear_color

    # --------- DRAW
    def drawColor(self, r, g, b):
        self.draw_color = color(r, g, b)

    # Dibujar un punto con coordenadas normalizadas
    def drawPoint_NDC(self, x, y, color=None):
        relative_x = self.vw_x + ((self.vw_width / 2) * (x + 1))
        relative_y = self.vw_y + ((self.vw_height / 2) * (y + 1))
        self.pixels[int(relative_x)][int(relative_y)] = color or self.draw_color

    def drawPoint(self, x, y, color=None):
        if x < self.vw_x or x > self.vw_x + self.vw_width or y < self.vw_y or y > self.vw_y + self.vw_height:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.draw_color

    # Bresenham's line algorithm
    # @arg: v0 → vértice inicial, v1 → vértice final
    def drawLine(self, v0, v1, color=None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        if x0 == x1 and y0 == y1:
            self.drawPoint(x0, y1, color)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Determinar si la línea está muy inclinada
        steep = dy > dx
        # Si la línea es demasiado inclinada, se cambian los valores
        # Normalmente y = mx + b, sin embargo, al tener una pendiente mayor
        # a 1, se pierden pixeles al momento de dibujar, por lo que se calcula
        # x = my + b
        if steep:
            # Intercambio de valores
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        # Define en qué punto se va dibujando en y
        offset = 0
        # Esto define cuál es el límite para cambiar de pixel
        limit = 0.5
        # Cálculo de la pendiente
        m = abs(y1 - y0) / abs(x1 - x0)
        y = y0
        for x in range(int(x0), int(x1 + 1)):
            if steep:
                self.drawPoint(y, x, color)
            else:
                self.drawPoint(x, y, color)
            # Cada cambio en x aumenta la pendiente a offset
            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1  # Indica el cambio de pixel (decisión)
                limit += 1

    def loadModel(self, filename, scale=V2(1, 1), translate=V2(0.0, 0.0)):

        model = obj.obj(filename)

        # draw Model
        for face in model.faces:
            vertex_count = len(face)  # Guarda la cantidad de vertices en la cara
            for x in range(vertex_count):
                # Se resta 0 porque OBJ empieza en 1 pero list empieza en 0
                index0 = face[x][0] - 1  # Obtiene el vértice de cada x
                index1 = face[(x + 1) % vertex_count][0] - 1  # Obtiene el índice del segundo vértice
                vertex0 = model.vertices[index0]  # Obtiene el vértice a dibujar con respecto a la cara
                vertex1 = model.vertices[index1]  # Obtiene el vértice a dibujar con respecto a la cara

                x0 = vertex0[0] * scale.x + translate.x
                y0 = vertex0[1] * scale.x + translate.x
                x1 = vertex1[0] * scale.x + translate.x
                y1 = vertex1[1] * scale.x + translate.x

                self.drawLine(V2(x0, y0), V2(x1, y1))


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
