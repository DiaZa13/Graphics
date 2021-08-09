# Cargar archivo OBJ
import struct

def color(r, g, b):
    # Comúnmente la tarjeta de video en colores acepta valor de 0 a 1
    # Y para convertirlo en byte se multiplica por 255
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:  # Por default open ya está en read-text
            self.lines = file.read().splitlines()  # Lee el documento línea por línea

        # Variables para almacenar la lectura del documento
        self.vertices = []
        self.textures = []  # Coordenadas de texturas
        self.normals = []
        self.faces = []

        self.saveData()

    def saveData(self):
        # Formato de OBJ
        # v -0.8523 -0.6325 -0.5238 → letra = prefijo, valores = coordenadas
        for line in self.lines:
            # Asegurar que la línea no está en blanco
            if line:
                prefix, value = line.split(' ', 1)  # Separar el prefijo del valor
                if prefix == 'v':  # Vertices
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':  # Coordenadas de textura
                    self.textures.append(value)
                elif prefix == 'vn':  # Normales
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(int, vertex.split('/'))) for vertex in value.split(' ')])


# Implementar texturas
class Texture(object):
    def __init__(self, filename):
        self.file = filename
        self.read()

    def read(self):
        # rb → abrir el archivo en modo lectura binario
        with open(self.file, 'rb') as img:
            # img.seek(10)  # Se salta 10bytes
            headerSize = struct.unpack('=1', img.read(4))[0]  # Para que lea el size del header

            img.seek(14 + 4)  # Se mueve a la posición en la que esta el ancho y el alto
            self.width = struct.unpack('=1', img.read(4))[0]  # Lee los 4bytes correspondientes del ancho
            self.height = struct.unpack('=1', img.read(4))[0]  # Lee los 4bytes correspondientes de la altura

            # Se necesitaba para empezar a leer la tabla de colores de la textura
            img.seek(headerSize)
            # Empezar a leer la imagen
            self.pixels = []  # Array de pixeles
            for x in range(self.width):
                self.pixels.append([])
                for y in range(self.height):
                    # Leyendo los colores de la textura
                    b = ord(img.read(1)) / 255  # ord → convierte el caracter a ascii
                    g = ord(img.read(1)) / 255  # /255 para asegurar que el valor va de 0-1
                    r = ord(img.read(1)) / 255
                    self.pixels[x].append(color(r, g, b))

    def getColor(self, tx, ty):
        if 0 <= tx < 1 and 0 <= ty < 1:
            # Porque las coordenadas de color no están normalizadas
            x = round(tx * self.width)
            y = round(ty * self.height)

            return self.pixels[x][y]
        else:
            # Si se pasan coordenas inválidas entonces se devuelve negro
            return color(0, 0, 0)

