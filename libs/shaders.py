from libs import zmath as zm
import numpy as np

# Lógica para hacer shaders

# key word arguments **kwargs → pasa un listado de argumentos con una llave
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

def gourad_shader(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    A, B, C = kwargs['vertx']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b /= 255
    g /= 255
    r /= 255

    a_intesity = np.dot(nA, [-i for i in render.directional_light])
    b_intesity = np.dot(nB, [-i for i in render.directional_light])
    c_intesity = np.dot(nC, [-i for i in render.directional_light])

    intensity = a_intesity * u + b_intesity * v + c_intesity * w

    if intensity > 1:
        intensity = 1
    elif intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    return r, g, b

