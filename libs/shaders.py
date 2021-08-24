from libs import zmath as zm

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
    tA, tB, tC = kwargs['textCoords']
    A, B, C = kwargs['vertx']
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

    if render.active_texture2:
        color = render.active_texture2.getColor(tx, ty)
        b += (color[0] / 255) * (1 - intensity)
        g += (color[1] / 255) * (1 - intensity)
        r += (color[2] / 255) * (1 - intensity)

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

    return r, g, b

    pass

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