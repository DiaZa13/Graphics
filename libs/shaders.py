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
        b *= color[0]/255
        g *= color[1]/255
        r *= color[2]/255

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
        b *= color[0]/255
        g *= color[1]/255
        r *= color[2]/255

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
        b *= color[0]/255
        g *= color[1]/255
        r *= color[2]/255

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
    A, B, C = kwargs['vertx']
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

    # Cálculo de iluminación
    normal = zm.cross(zm.subtract(B, A), zm.subtract(C, A))
    normal = zm.normalize(normal)  # normalización
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
        if ((x + 1) * 1/8) % 2 > 1 and (y * 1/8) % 2 > 1:
            b = 0
            g = 0
            r = intensity
        elif ((x + 1) * 1/8) % 2 < 1 and (y * 1/8) % 2 < 1:
            b = 0
            g = 0
            r = intensity
    if y % 8 == 0:
        if (x * 1/8) % 2 > 1 and ((y + 1) * 1/8) % 2 > 1:
            b = 0
            g = 0
            r = intensity
        elif (x * 1/8) % 2 < 1 and ((y + 1) * 1/8) % 2 < 1:
            b = 0
            g = 0
            r = intensity
    elif (x * 1/8) % 2 > 1 and (y * 1/8) % 2 > 1:
        b = 0
        g = 0
        r = intensity
    elif (x * 1/8) % 2 < 1 and (y * 1/8) % 2 < 1:
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
        if ((x + 1) * 1/4) % 2 > 1:
            b *= intensity
            g *= intensity
            r *= intensity
    elif (x * 1/4) % 2 > 1 and (y * 1/4) % 2 > 1:
        b *= intensity
        g *= intensity
        r *= intensity

    return r, g, b

def bw_static(render, **kwargs):
    WHITE = _color(220/255, 220/255, 220/255)
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
    WHITE = _color(220/255, 220/255, 220/255)
    YELLOW = _color(238/255, 207/255, 7/255)
    CYAN = _color(37/255, 215/255, 237/255)
    GREEN = _color(4/255, 155/255, 32/255)
    MAGENTA = _color(235/255, 79/255, 190/255)
    RED = _color(164/255, 10/255, 10/255)
    BLUE = _color(14/255, 41/255, 191/255)
    GRAY = _color(97/255, 92/255, 99/255)

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

    if x % 25 == 0:
        if 0 <= (x * 1 / 25) % 7 < 1:
            b += WHITE[0] * intensity
            g += WHITE[1] * intensity
            r += WHITE[2] * intensity
        elif 1 <= (x * 1 / 25) % 7 < 2:
            b += YELLOW[0] * intensity
            g += YELLOW[1] * intensity
            r += YELLOW[2] * intensity
        elif 2 <= (x * 1 / 25) % 7 < 3:
            b += CYAN[0] * intensity
            g += CYAN[1] * intensity
            r += CYAN[2] * intensity
        elif 3 <= (x * 1 / 25) % 7 < 4:
            b += GREEN[0] * intensity
            g += GREEN[1] * intensity
            r += GREEN[2] * intensity
        elif 4 <= (x * 1 / 25) % 7 < 5:
            b += MAGENTA[0] * intensity
            g += MAGENTA[1] * intensity
            r += MAGENTA[2] * intensity
        elif 5 <= (x * 1 / 25) % 7 < 6:
            b += RED[0] * intensity
            g += RED[1] * intensity
            r += RED[2] * intensity
        elif 6 <= (x * 1 / 25) % 7 < 7:
            b += BLUE[0] * intensity
            g += BLUE[1] * intensity
            r += BLUE[2] * intensity
    elif 0 <= (x * 1 / 25) % 7 < 1:
        b += WHITE[0] * intensity
        g += WHITE[1] * intensity
        r += WHITE[2] * intensity
    elif 1 <= (x * 1 / 25) % 7 < 2:
        b += YELLOW[0] * intensity
        g += YELLOW[1] * intensity
        r += YELLOW[2] * intensity
    elif 2 <= (x * 1 / 25) % 7 < 3:
        b += CYAN[0] * intensity
        g += CYAN[1] * intensity
        r += CYAN[2] * intensity
    elif 3 <= (x * 1 / 25) % 7 < 4:
        b += GREEN[0] * intensity
        g += GREEN[1] * intensity
        r += GREEN[2] * intensity
    elif 4 <= (x * 1 / 25) % 7 < 5:
        b += MAGENTA[0] * intensity
        g += MAGENTA[1] * intensity
        r += MAGENTA[2] * intensity
    elif 5 <= (x * 1 / 25) % 7 < 6:
        b += RED[0] * intensity
        g += RED[1] * intensity
        r += RED[2] * intensity
    elif 6 <= (x * 1 / 25) % 7 < 7:
        b += BLUE[0] * intensity
        g += BLUE[1] * intensity
        r += BLUE[2] * intensity

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
    light_ambient_color = (1, 1, 0.2)
    light_diffuse_color = (1, 1, 1)
    light_specular_color = (1, 1, 1)
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

    intensity = [ambient[0] + diffuse[0] + specular[0], ambient[1] + diffuse[1] + specular[1], ambient[2] + diffuse[2] + specular[2]]
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


def normal_map(render, **kwargs):
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

    # Calculo de la normal del pixel
    normal = (nx, ny, nz)

    if render.normal_map:
        textNormal = render.normal_map.getColor(tx, ty)
        # Para asegurar que esta en un rango de 0 → 1
        textNormal = [(textNormal[2] / 255) * 2 -1,
                      (textNormal[1] / 255) * 2 -1,
                      (textNormal[0] / 255) * 2 -1]
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