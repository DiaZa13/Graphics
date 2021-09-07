# Graphic library
from collections import namedtuple
from libs.zutils import char, word, dword, _color, baryCoords
from libs.obj import Obj, Texture
from numpy import tan
from libs import zmath as zm


# Creación de un tipo de variable para dibujar una línea
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

# COLORS
BLACK = _color(0, 0, 0)
WHITE = _color(1, 1, 1)


# Creación de clase para hacer renderizar
class Raytracer(object):
    def __init__(self, width, height):  # constructor
        # Las variables se crean dentro del constructor
        self.draw_color = WHITE
        self.clear_color = BLACK
        # Window size
        self.width = width
        self.height = height
        self.createWindow()
        # Dirección de luz original
        self.directional_light = V3(0, 0, -1)
        self.camPosition = V3(0, 0, 0)
        self.fov = 60

        # Agrega los objetos que se quieren renderizar en pantalla
        self.scene = []

        self.pointLight = None
    # -------- CLEAR
    # Define el color con el que se va a limpiar la pantalla
    def clearColor(self, r, g, b):
        self.clear_color = _color(r, g, b)

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
        self.draw_color = _color(r / 255, g / 255, b / 255)

    def drawPoint(self, x, y, color=None):
        if x < self.vw_x or x > self.vw_x + self.vw_width or y < self.vw_y or y > self.vw_y + self.vw_height:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.draw_color

    def loadModel(self, filename, scale=V3(1, 1, 1), translate=V3(0, 0, 0), rotate=V3(0, 0, 0)):

        model = Obj(filename)
        modelMatrix = self.objectMatriz(translate, scale, rotate)
        rotationMatrix = self.CreateRotationMatrix(rotate)

        # draw Model
        for face in model.faces:
            vertex_count = len(face)  # Guarda la cantidad de vertices en la cara

            # Vértices transformados por la matriz del modelo
            vert, vt, vn = [], [], []
            for i in range(vertex_count):
                vertex = model.vertices[face[i][0] - 1]
                a = self.transform(vertex, modelMatrix)
                vert.append(a)
                # Coordenadas de textura
                vt.append(model.textures[face[i][1] - 1])
                # Normales
                # Las normales que devuelve el modelo son antes de haber
                # rotado el objeto. Para tener las normales correctas
                # hay que asegurar que también están rotadas
                normal = model.normals[face[i][2] - 1]
                a = self.transform_direction(normal, rotationMatrix)
                vn.append(a)

            # Transformación de vértices por la cámara
            a = self.camTransform(vert[0])
            b = self.camTransform(vert[1])
            c = self.camTransform(vert[2])
            if vertex_count == 4:
                d = self.camTransform(vert[3])

            # Dibuja los vértices
            self.drawTriangle_bc(a, b, c, textCoords=(vt[0], vt[1], vt[2]), normals=(vn[0], vn[1], vn[2]),
                                 vertx=(vert[0], vert[1], vert[2]))

            if vertex_count == 4:
                self.drawTriangle_bc(a, c, d, textCoords=(vt[0], vt[2], vt[3]), normals=(vn[0], vn[2], vn[3]),
                                     vertx=(vert[0], vert[1], vert[2]))

    def render(self):
        for y in range(0, self.height, 2):
            for x in range(0, self.height, 2):  # Convertir de world coordinates a NCD
                px = 2 * ((x + 1/2) / self.width) - 1  # Se le suma 1/2 al pixel para que al momento de generar los
                py = 2 * ((y + 1/2) / self.height) - 1  # rayos desde los pixeles el mismo se genere desde en el centro
                # Simulación del ángulo de visión, asumiendo que el near plane está a 1 unidad de la cámara
                aRatio = self.width / self.height
                t = tan(zm.deg2rad(self.fov) / 2)
                r = t * aRatio
                # Calcular posición de los pixeles en un espacio 3D
                px *= r
                py *= t

                # Dirección del rayo
                # La cámara siempre está viendo hacia -Z
                dirRay = V3(px, py, -1)
                dirRay = zm.normalize(dirRay)
                # El origen del rayo es la posición de la cámara
                self.drawPoint(x, y, self.castRay(self.camPosition, dirRay))

    def castRay(self, origin, direction):
        material = self.sceneIntersect(origin, direction)
        if material is None:
            return self.clear_color
        else:
            return material.diffuse

    def sceneIntersect(self, origin, direction):
        depth = float("inf")
        material = None
        for figure in self.scene:
            intersect = figure.rayIntersect(origin, direction)
            if intersect is not None:
                if intersect.distance < depth:
                    material = figure.material
                    depth = intersect.distance

        return material
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
