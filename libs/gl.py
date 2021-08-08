# Graphic library
from collections import namedtuple
from libs.zutils import char, word, dword, color, baryCoords
from libs import obj
import random

# Creación de un tipo de variable para dibujar una línea
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'Z'])

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

        # Revisar
        self.zbufer = [[-float('inf') for y in range(self.height)] for x in range(self.width)]

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
        self.draw_color = color(r/255, g/255, b/255)

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

    # ------- TRIANGLES
    # Dibujado de triángulos
    def flatBottomTriangle(self, v1, v2, v3, color=None):
        # Pendientes
        m21 = (v2.x - v1.x) / (v2.y - v1.y)
        m31 = (v3.x - v1.x) / (v3.y - v1.y)
        x1 = v2.x
        x2 = v3.x

        for y in range(v2.y, v1.y + 1):
            self.drawLine(V2(int(x1), y), V2(int(x2), y), color)
            x1 += m21
            x2 += m31

    def flatTopTriangle(self, v1, v2, v3, color=None):
        m31 = (v3.x - v1.x) / (v3.y - v1.y)
        m32 = (v3.x - v2.x) / (v3.y - v2.y)
        x1 = v3.x
        x2 = v3.x

        for y in range(v3.y, v1.y + 1):
            self.drawLine(V2(int(x1), y), V2(int(x2), y), color)
            x1 += m31
            x2 += m32

    def drawTriangle(self, A, B, C, color=None):
        # Ordenar descendentemente los vértices del triángulo → arriba hacia abajo
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        if B.y == C.y:  # Triángulo normal → base inferior plana
            self.flatBottomTriangle(A, B, C, color)
        elif A.y == B.y:  # Triángulo invertido → base superior plana
            self.flatTopTriangle(A, B, C, color)
        else:  # Triángulo irregular
            # 1. Dividir el triángulo en 2
            # 2. Dibujar ambos casos TN y TI
            # Teorema de intercepto para sacar el reflejo de B
            x = A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x)
            D = V2(x, B.y)
            self.flatBottomTriangle(A, B, D, color)
            self.flatTopTriangle(D, B, C, color)
            pass

    def drawTriangle_bc(self, A, B, C, color=None):
        # Bounding Box → límites
        y_max = round(max(A.y, B.y, C.y))
        y_min = round(min(A.y, B.y, C.y))
        x_max = round(max(A.x, B.x, C.x))
        x_min = round(min(A.x, B.x, C.x))

        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))

                if u >= 0 and v >= 0 and w >= 0:
                    # Conocer el valor de z
                    z = A.z * u + B.z * v + C.z * w
                    if z > self.zbuffer[x][y]:
                        self.drawPoint(x, y)
                        # Modifico el valor del zbuffer
                        self.zbufer[x][y] = z

    # ----------- OBJ
    def loadModel(self, filename, scale=V2(1, 1), translate=V2(0.0, 0.0)):

        model = obj.obj(filename)

        # draw Model
        for face in model.faces:
            vertex_count = len(face)  # Guarda la cantidad de vertices en la cara

            if vertex_count == 3:
                index0 = face[0][0] - 1  # Obtiene el vértice de cada x
                index1 = face[1][0] - 1  # Obtiene el vértice de cada x
                index2 = face[2][0] - 1  # Obtiene el vértice de cada x

                vert0 = model.vertices[index0]
                vert1 = model.vertices[index1]
                vert2 = model.vertices[index2]

                a = V2(int(vert0[0] * scale.x + translate.x), int(vert0[1] * scale.y + translate.y))
                b = V2(int(vert1[0] * scale.x + translate.x), int(vert1[1] * scale.y + translate.y))
                c = V2(int(vert2[0] * scale.x + translate.x), int(vert2[1] * scale.y + translate.y))

                self.drawTriangle(a, b, c, color(random.random(), random.random(),random.random()))


    def transform(self, vertex, translate=V3(0, 0, 0), scale=V3(1,1,1)):
        return V3(vertex[0] * scale.x + translate.x)
        return V3(vertex[0] * scale.y + translate.y)
        return V3(vertex[0] * scale.z + translate.z)

    # Rellenado de polígonos
    def filling(self, polygon, clase=None):
        limit = len(polygon)
        x_coordinates = []
        y_coordinates = []
        slopes = []
        drawX = []
        for v in polygon:
            x_coordinates.append(v[0])
            y_coordinates.append(v[1])

        y_max = max(y_coordinates)
        y_min = min(y_coordinates)

        for v in range(limit):
            x0 = polygon[v][0]
            y0 = polygon[v][1]
            x1 = polygon[(v + 1) % limit][0]
            y1 = polygon[(v + 1) % limit][1]

            m = (y1 - y0) / (x1 - x0)

            slopes.append(m)

        for y in range(y_min, y_max):

            for v in range(limit):
                a = polygon[v][1]
                b = polygon[(v + 1) % limit][1]
                x = polygon[v][0]
                if (a <= y < b) or (b <= y < a):
                    x = round(((y - a) / slopes[v]) + x)
                    drawX.append(x)

            self.drawLine(V2(drawX[(len(drawX) - 2)], y), V2(drawX[len(drawX) - 1], y))
            if clase == 'e':
                if y_min <= y < 345:
                    self.drawLine(V2(drawX[(len(drawX) - 4)], y), V2(drawX[len(drawX) - 3], y))
                    self.drawLine(V2(drawX[(len(drawX) - 2)], y), V2(drawX[len(drawX) - 1], y))
            elif clase == 't':
                if 144 <= y < 177:
                    self.drawLine(V2(drawX[(len(drawX) - 4)], y), V2(drawX[len(drawX) - 3], y))
                    self.drawLine(V2(drawX[(len(drawX) - 2)], y), V2(drawX[len(drawX) - 1], y), color(0, 0, 0))
                elif 177 <= y < 180:
                    self.drawLine(V2(drawX[(len(drawX) - 4)], y), V2(drawX[len(drawX) - 3], y))

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