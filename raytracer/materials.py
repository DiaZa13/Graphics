import libs.zutils as zu

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Materials(object):
    def __init__(self, diffuse=zu.WHITE, spec=1, material_type=OPAQUE):
        # diffuse = color de la superficie
        self.diffuse = diffuse
        self.spec = spec
        self.material_type = material_type


# default materials
SKY = Materials(diffuse=zu.colors(135 / 255, 206 / 255, 235 / 255), spec=64)
GRASS = Materials(diffuse=zu.colors(86 / 255, 125 / 255, 70 / 255), spec=128)
COPPER = Materials(diffuse=zu.colors(168 / 255, 98 / 255, 66 / 255))
STONE = Materials(diffuse=zu.colors(0.4, 0.4, 0.4), spec=64)
MIRROR = Materials(material_type=REFLECTIVE)

