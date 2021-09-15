import libs.zutils as zu


class Materials(object):
    def __init__(self, diffuse=zu.WHITE):
        # diffuse = color de la superficie
        self.diffuse = diffuse


# default materials
SKY = Materials(zu.colors(135 / 255, 206 / 255, 235 / 255))
GRASS = Materials(zu.colors(86 / 255, 125 / 255, 70 / 255))
COPPER = Materials(zu.colors(168 / 255, 98 / 255, 66 / 255))

