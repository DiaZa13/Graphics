import libs.zutils as zu


class Materials(object):
    def __init__(self, diffuse=zu.WHITE, spec=1):
        # diffuse = color de la superficie
        self.diffuse = diffuse
        self.spec = spec


# default materials
SKY = Materials(diffuse=zu.colors(135 / 255, 206 / 255, 235 / 255), spec=64)
GRASS = Materials(diffuse=zu.colors(86 / 255, 125 / 255, 70 / 255), spec=128)
COPPER = Materials(diffuse=zu.colors(168 / 255, 98 / 255, 66 / 255))
STONE = Materials(diffuse=zu.colors(0.4, 0.4, 0.4), spec=64)

