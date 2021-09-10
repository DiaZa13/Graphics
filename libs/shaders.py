from libs import zmath as zm
from libs.zutils import _color
from numpy import cos, sin


# Lógica para hacer shaders

# key word arguments **kwargs → pasa un listado de argumentos con una llave
# La iluminación se calcula por primitiva → tipo de polígono con el que se
def flat_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    A, B, C = kwargs['vertx']
    b, g, r = kwargs['color']
    light_diffuse_color = (1, 1, 1)

    # Asegurarme que los colores están únicamente de 0 a 1
    b /= 255
    g /= 255
    r /= 255

    # Cálculo de iluminación
    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
    diffuseIntensity = max(zm.dot(normal, [-i for i in render.directional_light]), 0)
    intensity = zm.dot(diffuseIntensity, light_diffuse_color)

    if intensity[0] > 1:
        intensity[0] = 1
    if intensity[1] > 1:
        intensity[1] = 1
    if intensity[2] > 1:
        intensity[2] = 1

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        color = [intensity[0] * (color[0] / 255), intensity[1] * (color[1] / 255), intensity[2] * (color[2] / 255)]

    b = color[0]
    g = color[1]
    r = color[2]

    return r, g, b

def flat_color_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    A, B, C = kwargs['vertx']
    b, g, r = kwargs['color']
    light_diffuse_color = (38 / 255, 185 / 255, 0.5)

    # Asegurarme que los colores están únicamente de 0 a 1
    b /= 255
    g /= 255
    r /= 255

    # Cálculo de iluminación
    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
    diffuseIntensity = max(zm.dot(normal, [-i for i in render.directional_light]), 0)
    intensity = zm.dot(diffuseIntensity, light_diffuse_color)

    if intensity[0] > 1:
        intensity[0] = 1
    if intensity[1] > 1:
        intensity[1] = 1
    if intensity[2] > 1:
        intensity[2] = 1

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        color = [intensity[0] * (color[0] / 255), intensity[1] * (color[1] / 255), intensity[2] * (color[2] / 255)]

    b = color[0]
    g = color[1]
    r = color[2]

    return r, g, b

# Calcula la iluminación por vértice
# Luego la iluminación calculada se interpola por cada pixel
def gourad_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b /= 255
    g /= 255
    r /= 255

    a_intesity = zm.dot(nA, [-i for i in render.directional_light])
    b_intesity = zm.dot(nB, [-i for i in render.directional_light])
    c_intesity = zm.dot(nC, [-i for i in render.directional_light])

    # Interpolación de intensidad
    intensity = a_intesity * u + b_intesity * v + c_intesity * w

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    return r, g, b


# Calcula la iluminación por pixel
# Luego la iluminación calculada se interpola por la normal
def phong_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']
    tA, tB, tC = kwargs['textCoords']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Interpolación de normales
    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nx, ny, nz)

    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    return r, g, b


# Básicamente es sin iluminación
def unlit_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    A, B, C = kwargs['vertx']
    tA, tB, tC = kwargs['textCoords']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    return r, g, b


# Los saltos de luz no son graduales sino inmediatos
def toon_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']
    A, B, C = kwargs['vertx']
    tA, tB, tC = kwargs['textCoords']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Interpolación de normales
    # nx = nA[0] * u + nB[0] * v + nC[0] * w
    # ny = nA[1] * u + nB[1] * v + nC[1] * w
    # nz = nA[2] * u + nB[2] * v + nC[2] * w
    #
    # normal = (nx, ny, nz)

    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización

    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 0.7:
        intensity = 1
    elif intensity > 0.4:
        intensity = 0.5
    else:
        intensity = 0.1

    b *= intensity
    g *= intensity
    r *= intensity

    return r, g, b


# Interpolar entre 2 texturas
def texture_interpol(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']
    A, B, C = kwargs['vertx']
    tA, tB, tC = kwargs['textCoords']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # # Interpolación de normales
    # nx = nA[0] * u + nB[0] * v + nC[0] * w
    # ny = nA[1] * u + nB[1] * v + nC[1] * w
    # nz = nA[2] * u + nB[2] * v + nC[2] * w
    #
    # normal = (nx, ny, nz)

    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
    intensity = zm.dot(normal, [-i for i in render.directional_light])

    # intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if render.active_texture2:
        color = render.active_texture2.getColor(tx, ty)
        b += (color[0] / 255) * (1 - intensity)
        g += (color[1] / 255) * (1 - intensity)
        r += (color[2] / 255) * (1 - intensity)

    return r, g, b


def lava_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']
    tA, tB, tC = kwargs['textCoords']
    x, y, z = kwargs['coordinates']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Interpolación de normales
    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nx, ny, nz)

    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if render.active_texture2:
        color = render.active_texture2.getColor(tx, ty)
        b += (color[0] / 255) * (1 - intensity)
        g += (color[1] / 255) * (1 - intensity)
        r += (color[2] / 255) * (1 - intensity)
        g *= x / 255
        b *= y / 255
        b /= 255
        g /= 255

    return r, g, b


def blue_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    A, B, C = kwargs['vertx']
    b, g, r = kwargs['color']

    # Asegurarme que los colores están únicamente de 0 a 1
    b /= 255
    g /= 255
    r /= 255

    # Cálculo de color de textura
    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Cálculo de iluminación
    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity
    b += 0.5
    b /= 255

    return r, g, b


def space_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    b, g, r = kwargs['color']
    x, y, z = kwargs['coordinates']
    nA, nB, nC = kwargs['normals']

    # Asegurarme que los colores están únicamente de 0 a 1
    b /= 255
    g /= 255
    r /= 255

    # Cálculo de color de textura
    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Interpolación de normales
    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nx, ny, nz)

    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    if x % 2 == 0 and y % 2 == 0:
        b *= intensity
        g *= intensity
        r *= intensity
    else:
        b = 0
        g = 0
        r = 0

    return r, g, b


def space_unlit_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    A, B, C = kwargs['vertx']
    tA, tB, tC = kwargs['textCoords']
    x, y, z = kwargs['coordinates']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Interpolación de normales
    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    if x % 2 == 0 and y % 2 == 0:
        b = 0
        g = 0
        r = 0
    else:
        b *= intensity
        g *= intensity
        r *= intensity

    return r, g, b


def checkers(render, **kwargs):
    A, B, C = kwargs['vertx']
    b, g, r = kwargs['color']
    x, y, z = kwargs['coordinates']

    # Asegurarme que los colores están únicamente de 0 a 1
    b /= 255
    g /= 255
    r /= 255

    # Cálculo de color de textura
    # if render.active_texture:
    #     tx = tA[0] * u + tB[0] * v + tC[0] * w
    #     ty = tA[1] * u + tB[1] * v + tC[1] * w
    #     color = render.active_texture.getColor(tx, ty)
    #     # Color actual por el color devuelto por la textura
    #     b *= color[0] / 255
    #     g *= color[1] / 255
    #     r *= color[2] / 255

    # Cálculo de iluminación
    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    # bright = (((x * .5) % 1) + 0.5) + (((y * .5) % 1) + 0.5)
    #
    # if bright % 2 == 0:
    #     b = 1
    #     g = 1
    #     r = 1

    # if x % 4 == 0:
    #     if ((x + 1) * 1/4) % 2 > 1:
    #         b = 1
    #         g = 1
    #         r = 1
    # elif (x * 1/4) % 2 > 1 and (y * 1/4) % 2 > 1:
    #     b = 1
    #     g = 1
    #     r = 1

    # if x % 4 == 0:
    #     if ((x + 1) * 1/4) % 2 > 1:
    #         b = 1
    #         g = 1
    #         r = 1
    # elif (x * 1/4 + y * 1/4) % 2 > 1 :
    #     b = 1
    #     g = 1
    #     r = 1

    if x % 8 == 0:
        if ((x + 1) * 1 / 8) % 2 > 1 and (y * 1 / 8) % 2 > 1:
            b = 0
            g = 0
            r = intensity
        elif ((x + 1) * 1 / 8) % 2 < 1 and (y * 1 / 8) % 2 < 1:
            b = 0
            g = 0
            r = intensity
    if y % 8 == 0:
        if (x * 1 / 8) % 2 > 1 and ((y + 1) * 1 / 8) % 2 > 1:
            b = 0
            g = 0
            r = intensity
        elif (x * 1 / 8) % 2 < 1 and ((y + 1) * 1 / 8) % 2 < 1:
            b = 0
            g = 0
            r = intensity
    elif (x * 1 / 8) % 2 > 1 and (y * 1 / 8) % 2 > 1:
        b = 0
        g = 0
        r = intensity
    elif (x * 1 / 8) % 2 < 1 and (y * 1 / 8) % 2 < 1:
        b = 0
        g = 0
        r = intensity
    else:
        b = intensity
        g = intensity
        r = intensity

    return r, g, b


def pattern(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    nA, nB, nC = kwargs['normals']
    b, g, r = kwargs['color']
    x, y, z = kwargs['coordinates']

    # Asegurarme que los colores están únicamente de 0 a 1
    b /= 255
    g /= 255
    r /= 255

    # Cálculo de color de textura
    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

        # Interpolación de normales
    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nx, ny, nz)

    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    # if x % 4 == 0:
    #     if ((x + 1) * 1/4) % 2 > 1:
    #         b *= intensity
    #         g *= intensity
    #         r *= intensity
    # elif (x * 1/4 + y * 1/4) % 2 > 1:
    #     b *= intensity
    #     g *= intensity
    #     r *= intensity

    if x % 4 == 0:
        if ((x + 1) * 1 / 4) % 2 > 1:
            b *= intensity
            g *= intensity
            r *= intensity
    elif (x * 1 / 4) % 2 > 1 and (y * 1 / 4) % 2 > 1:
        b *= intensity
        g *= intensity
        r *= intensity

    return r, g, b


def bw_static(render, **kwargs):
    WHITE = _color(220 / 255, 220 / 255, 220 / 255)
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']
    tA, tB, tC = kwargs['textCoords']
    x, y, z = kwargs['coordinates']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Interpolación de normales
    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nx, ny, nz)

    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    if x % 2 == 0 and y % 2 == 0 and (x + y) % 3 == 0:
        b = intensity
        g = intensity
        r = intensity
    else:
        b *= WHITE[0]
        g *= WHITE[1]
        r *= WHITE[2]

    b /= 255
    g /= 255
    r /= 255

    return r, g, b


def static(render, **kwargs):
    WHITE = _color(220 / 255, 220 / 255, 220 / 255)
    YELLOW = _color(238 / 255, 207 / 255, 7 / 255)
    CYAN = _color(37 / 255, 215 / 255, 237 / 255)
    GREEN = _color(4 / 255, 155 / 255, 32 / 255)
    MAGENTA = _color(235 / 255, 79 / 255, 190 / 255)
    RED = _color(164 / 255, 10 / 255, 10 / 255)
    BLUE = _color(14 / 255, 41 / 255, 191 / 255)

    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    A, B, C = kwargs['vertx']
    tA, tB, tC = kwargs['textCoords']
    x, y, z = kwargs['coordinates']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # # Interpolación de normales
    # nx = nA[0] * u + nB[0] * v + nC[0] * w
    # ny = nA[1] * u + nB[1] * v + nC[1] * w
    # nz = nA[2] * u + nB[2] * v + nC[2] * w
    #
    # normal = (nx, ny, nz)

    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización

    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    if x % 25 == 0:
        if 0 <= (x * 1 / 25) % 7 < 1:
            b *= WHITE[0]
            g *= WHITE[1]
            r *= WHITE[2]
        elif 1 <= (x * 1 / 25) % 7 < 2:
            b *= YELLOW[0]
            g *= YELLOW[1]
            r *= YELLOW[2]
        elif 2 <= (x * 1 / 25) % 7 < 3:
            b *= CYAN[0]
            g *= CYAN[1]
            r *= CYAN[2]
        elif 3 <= (x * 1 / 25) % 7 < 4:
            b *= GREEN[0]
            g *= GREEN[1]
            r *= GREEN[2]
        elif 4 <= (x * 1 / 25) % 7 < 5:
            b *= MAGENTA[0]
            g *= MAGENTA[1]
            r *= MAGENTA[2]
        elif 5 <= (x * 1 / 25) % 7 < 6:
            b *= RED[0]
            g *= RED[1]
            r *= RED[2]
        elif 6 <= (x * 1 / 25) % 7 < 7:
            b *= BLUE[0]
            g *= BLUE[1]
            r *= BLUE[2]
    elif 0 <= (x * 1 / 25) % 7 < 1:
        b *= WHITE[0]
        g *= WHITE[1]
        r *= WHITE[2]
    elif 1 <= (x * 1 / 25) % 7 < 2:
        b *= YELLOW[0]
        g *= YELLOW[1]
        r *= YELLOW[2]
    elif 2 <= (x * 1 / 25) % 7 < 3:
        b *= CYAN[0]
        g *= CYAN[1]
        r *= CYAN[2]
    elif 3 <= (x * 1 / 25) % 7 < 4:
        b *= GREEN[0]
        g *= GREEN[1]
        r *= GREEN[2]
    elif 4 <= (x * 1 / 25) % 7 < 5:
        b *= MAGENTA[0]
        g *= MAGENTA[1]
        r *= MAGENTA[2]
    elif 5 <= (x * 1 / 25) % 7 < 6:
        b *= RED[0]
        g *= RED[1]
        r *= RED[2]
    elif 6 <= (x * 1 / 25) % 7 < 7:
        b *= BLUE[0]
        g *= BLUE[1]
        r *= BLUE[2]

    if y % 2 == 0:
        b = intensity
        g = intensity
        r = intensity

    b = b / 255
    g = g / 256
    r = r / 256

    return r, g, b


def texture_intensity(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']
    tA, tB, tC = kwargs['textCoords']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture2:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Interpolación de normales
    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nx, ny, nz)
    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if render.active_texture:
        color = render.active_texture2.getColor(tx, ty)
        b += (color[0] / 255) * (1 - intensity)
        g += (color[1] / 255) * (1 - intensity)
        r += (color[2] / 255) * (1 - intensity)

    return r, g, b


def blinn_phong_reflection(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']
    tA, tB, tC = kwargs['textCoords']
    x, y, z = kwargs['coordinates']
    A, B, C = kwargs['vertx']
    light_ambient_color = (38 / 255, 185 / 255, 0.2)
    light_diffuse_color = (1, 1, 1)
    light_specular_color = (38 / 255, 185 / 255, 0.2)
    position = [x, y, z]

    # Ambient light
    ambientIntensity = 0.1
    ambient = zm.dot(ambientIntensity, light_ambient_color)

    # Diffuse light
    # Interpolación de normales
    # nx = nA[0] * u + nB[0] * v + nC[0] * w
    # ny = nA[1] * u + nB[1] * v + nC[1] * w
    # nz = nA[2] * u + nB[2] * v + nC[2] * w

    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
    diffuseIntensity = max(zm.dot(normal, [-i for i in render.directional_light]), 0)
    diffuse = zm.dot(diffuseIntensity, light_diffuse_color)

    # Specular light
    viewDir = zm.normalize(zm.subtract(render.camPosition, position))
    halfwayDir = zm.normalize(zm.sum(render.directional_light, viewDir))
    specularIntensity = pow(max(zm.dot(normal, halfwayDir), 0), 16)
    specular = zm.dot(specularIntensity, light_specular_color)

    intensity = [ambient[0] + diffuse[0] + specular[0], ambient[1] + diffuse[1] + specular[1],
                 ambient[2] + diffuse[2] + specular[2]]
    if intensity[0] > 1:
        intensity[0] = 1
    if intensity[1] > 1:
        intensity[1] = 1
    if intensity[2] > 1:
        intensity[2] = 1

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        color = [intensity[0] * (color[0] / 255), intensity[1] * (color[1] / 255), intensity[2] * (color[2] / 255)]
        b = color[0]
        g = color[1]
        r = color[2]

    return r, g, b


def glow_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    A, B, C = kwargs['vertx']
    b, g, r = kwargs['color']
    glow_color = (1, 233 / 255, 0)

    # Asegurarme que los colores están únicamente de 0 a 1
    b /= 255
    g /= 255
    r /= 255

    # Cálculo de color de textura
    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Cálculo de iluminación
    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    camForward = [render.camMatrix.matrix[0][2],
                  render.camMatrix.matrix[1][2],
                  render.camMatrix.matrix[2][2]]

    glowIntensity = 1 - zm.dot(normal, camForward)

    r += glow_color[0] * glowIntensity
    g += glow_color[1] * glowIntensity
    b += glow_color[2] * glowIntensity

    if b > 1:
        b = 1
    if g > 1:
        g = 1
    if r > 1:
        r = 1

    return r, g, b


def normal_map(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    A, B, C = kwargs['vertx']
    nA, nB, nC = kwargs['normals']
    tA, tB, tC = kwargs['textCoords']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        color = render.active_texture.getColor(tx, ty)
        # Color actual por el color devuelto por la textura
        b *= color[0] / 255
        g *= color[1] / 255
        r *= color[2] / 255

    # Interpolación de normales
    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w

    # Calculo de la normal del pixel
    normal = (nx, ny, nz)

    if render.normal_map:
        textNormal = render.normal_map.getColor(tx, ty)
        # Para asegurar que esta en un rango de 0 → 1
        textNormal = [(textNormal[2] / 255) * 2 - 1,
                      (textNormal[1] / 255) * 2 - 1,
                      (textNormal[0] / 255) * 2 - 1]

        edg1 = zm.subtract(B, A)
        edg2 = zm.subtract(C, A)
        deltav1 = zm.subtract(tB, tA)
        deltav2 = zm.subtract(tC, tA)

        f = 1 / deltav1[0] * deltav2[1] - deltav2[0] * deltav1[1]
        tangent = [f * (deltav2[1] * edg1[0] - deltav1[1] * edg2[0]),
                   f * (deltav2[1] * edg1[1] - deltav1[1] * edg2[1]),
                   f * (deltav2[1] * edg1[2] - deltav1[1] * edg2[2])]
        tangent = zm.normalize(tangent)
        btangent = zm.cross(normal, tangent)
        btangent = zm.normalize(btangent)

        tangentMatriz = zm.Matrix([[tangent[0], btangent[0], normal[0]],
                                   [tangent[1], btangent[1], normal[1]],
                                   [tangent[2], btangent[2], normal[2]]])

        light = tangentMatriz @ render.directional_light
        light = light.matrix[0]
        intensity = zm.dot(textNormal, [-i for i in light])
    else:
        # La intensidad se queda como que el shader es phong
        intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    return r, g, b

def normal_textures(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    A, B, C = kwargs['vertx']
    nA, nB, nC = kwargs['normals']
    nA2, nB2, nC2 = kwargs['normals2']
    tA, tB, tC = kwargs['textCoords']
    tA2, tB2, tC2 = kwargs['textCoords2']
    texture2 = kwargs['texture2']

    b /= 255
    g /= 255
    r /= 255

    edg1 = zm.subtract(B, A)
    edg2 = zm.subtract(C, A)

    # Interpolación de normales:
    if not texture2:
        if render.active_texture:
            tx = tA[0] * u + tB[0] * v + tC[0] * w
            ty = tA[1] * u + tB[1] * v + tC[1] * w
            color = render.active_texture.getColor(tx, ty)
            # Color actual por el color devuelto por la textura
            b *= color[0] / 255
            g *= color[1] / 255
            r *= color[2] / 255
        if render.normal_map:
            textNormal = render.normal_map.getColor(tx, ty)
            # Para asegurar que esta en un rango de 0 → 1
            textNormal = [(textNormal[2] / 255) * 2 - 1,
                          (textNormal[1] / 255) * 2 - 1,
                          (textNormal[0] / 255) * 2 - 1]

        deltav1 = zm.subtract(tB, tA)
        deltav2 = zm.subtract(tC, tA)
        # Normales de la primera textura
        nx = nA[0] * u + nB[0] * v + nC[0] * w
        ny = nA[1] * u + nB[1] * v + nC[1] * w
        nz = nA[2] * u + nB[2] * v + nC[2] * w

    else:
        if render.active_texture2:
            tx = tA2[0] * u + tB2[0] * v + tC2[0] * w
            ty = tA2[1] * u + tB2[1] * v + tC2[1] * w
            color = render.active_texture2.getColor(tx, ty)
            b *= (color[0] / 255)
            g *= (color[1] / 255)
            r *= (color[2] / 255)
        if render.normal_map2:
            textNormal = render.normal_map2.getColor(tx, ty)
            # Para asegurar que esta en un rango de 0 → 1
            textNormal = [(textNormal[2] / 255) * 2 - 1,
                          (textNormal[1] / 255) * 2 - 1,
                          (textNormal[0] / 255) * 2 - 1]

        deltav1 = zm.subtract(tB2, tA2)
        deltav2 = zm.subtract(tC2, tA2)
        # Normales de la segunda textura
        nx = nA2[0] * u + nB2[0] * v + nC2[0] * w
        ny = nA2[1] * u + nB2[1] * v + nC2[1] * w
        nz = nA2[2] * u + nB2[2] * v + nC2[2] * w

    normal = (nx, ny, nz)

    try:
        f = 1 / (deltav1[0] * deltav2[1] - deltav2[0] * deltav1[1])

        tangent = [f * (deltav2[1] * edg1[0] - deltav1[1] * edg2[0]),
                   f * (deltav2[1] * edg1[1] - deltav1[1] * edg2[1]),
                   f * (deltav2[1] * edg1[2] - deltav1[1] * edg2[2])]
        tangent = zm.normalize(tangent)
        btangent = zm.cross(normal, tangent)
        btangent = zm.normalize(btangent)
        tangentMatriz = zm.Matrix([[tangent[0], btangent[0], normal[0]],
                                   [tangent[1], btangent[1], normal[1]],
                                   [tangent[2], btangent[2], normal[2]]])

        light = tangentMatriz @ render.directional_light
        light = light.matrix[0]
        intensity = zm.dot(textNormal, [-i for i in light])
    except ZeroDivisionError:
        intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if b > 1:
        b = 1
    if g > 1:
        g = 1
    if r > 1:
        r = 1

    return r, g, b

def textures(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    A, B, C = kwargs['vertx']
    nA, nB, nC = kwargs['normals']
    nA2, nB2, nC2 = kwargs['normals2']
    tA, tB, tC = kwargs['textCoords']
    tA2, tB2, tC2 = kwargs['textCoords2']
    texture2 = kwargs['texture2']

    b /= 255
    g /= 255
    r /= 255

    # Validación de qué modelo se está dibujando
    if not texture2:
        if render.active_texture:
            tx = tA[0] * u + tB[0] * v + tC[0] * w
            ty = tA[1] * u + tB[1] * v + tC[1] * w
            color = render.active_texture.getColor(tx, ty)
            # Color actual por el color devuelto por la textura
            b *= color[0] / 255
            g *= color[1] / 255
            r *= color[2] / 255
        if render.normal_map:
            textNormal = render.normal_map.getColor(tx, ty)
            # Para asegurar que esta en un rango de 0 → 1
            textNormal = [(textNormal[2] / 255) * 2 - 1,
                          (textNormal[1] / 255) * 2 - 1,
                          (textNormal[0] / 255) * 2 - 1]
        # Normales de la primera textura
        nx = nA[0] * u + nB[0] * v + nC[0] * w
        ny = nA[1] * u + nB[1] * v + nC[1] * w
        nz = nA[2] * u + nB[2] * v + nC[2] * w

    else:
        if render.active_texture2:
            tx = tA2[0] * u + tB2[0] * v + tC2[0] * w
            ty = tA2[1] * u + tB2[1] * v + tC2[1] * w
            color = render.active_texture2.getColor(tx, ty)
            b *= (color[0] / 255)
            g *= (color[1] / 255)
            r *= (color[2] / 255)
        if render.normal_map2:
            textNormal = render.normal_map.getColor(tx, ty)
            # Para asegurar que esta en un rango de 0 → 1
            textNormal = [(textNormal[2] / 255) * 2 - 1,
                          (textNormal[1] / 255) * 2 - 1,
                          (textNormal[0] / 255) * 2 - 1]
        # Normales de la segunda textura
        nx = nA2[0] * u + nB2[0] * v + nC2[0] * w
        ny = nA2[1] * u + nB2[1] * v + nC2[1] * w
        nz = nA2[2] * u + nB2[2] * v + nC2[2] * w

    normal = (nx, ny, nz)
    intensity = zm.dot(normal, [-i for i in render.directional_light])

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if b > 1:
        b = 1
    if g > 1:
        g = 1
    if r > 1:
        r = 1

    return r, g, b
