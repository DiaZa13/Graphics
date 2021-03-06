import libs.zutils as zu
import libs.zmath as zm
from rasterizador.obj import Texture

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Materials(object):
    def __init__(self, diffuse=zu.WHITE, spec=1, ior=1, texture=None, material_type=OPAQUE):
        # diffuse = color de la superficie
        self.diffuse = diffuse
        self.spec = spec
        self.material_type = material_type
        self.ambientLight = None
        self.directionalLight = None
        self.pointLights = None
        self.intersect = None
        self.camPosition = None
        self.scene = None
        self.ior = ior
        self.texture = texture

    def objectLightning(self, scene, intersect):
        self.scene = scene
        self.ambientLight = scene.ambientLight
        self.directionalLight = scene.directionalLight
        self.pointLights = scene.pointLights
        self.intersect = intersect
        self.camPosition = scene.camPosition

    def opaqueMaterial(self):
        intensity = [0, 0, 0]

        if self.ambientLight:
            intensity = zm.sum(intensity, self.ambientLight.getColor())

        if self.directionalLight:
            directionalIntensity = self.directionalLight.getColor(self.intersect, self.camPosition, self.scene)
            intensity = zm.sum(intensity, directionalIntensity)

        for pointLight in self.pointLights:
            pointLightIntensity = pointLight.getColor(self.intersect, self.camPosition, self.scene)
            intensity = zm.sum(intensity, pointLightIntensity)

        return intensity




# default materials
SKY = Materials(diffuse=zu.colors(135 / 255, 206 / 255, 235 / 255), spec=16)
GRASS = Materials(diffuse=zu.colors(86 / 255, 125 / 255, 70 / 255), spec=128)
STONE = Materials(diffuse=zu.colors(0.4, 0.4, 0.4), spec=64)
WOOD = Materials(diffuse=(0.6, 0.2, 0.2), spec=64)
# REFLECTIVE MATERIALS
MIRROR = Materials(spec=128, material_type=REFLECTIVE)
GOLD = Materials(diffuse=zu.colors(1, 0.8, 0), spec=32, material_type=REFLECTIVE)
COPPER = Materials(diffuse=zu.colors(168 / 255, 98 / 255, 66 / 255), spec=16, material_type=REFLECTIVE)
ALUMINUM = Materials(diffuse=zu.colors(210 / 255, 217 / 255, 219 / 255), spec=128, material_type=REFLECTIVE)
METALLIC = Materials(diffuse=zu.colors(170 / 255, 169 / 255, 173 / 255), spec=128, material_type=REFLECTIVE)
NEON_YELLOW = Materials(diffuse=zu.colors(1, 243 / 255, 0), spec=128, material_type=REFLECTIVE)
# TRANSPARENT MATERIALS
GLASS = Materials(spec=64, ior=1.5, material_type=TRANSPARENT)
ICE = Materials(spec=128, ior=1.31, material_type=TRANSPARENT)
QUARTZ = Materials(spec=32, ior=1.46, material_type=TRANSPARENT)
SAPPHIRE = Materials(spec=32, ior=1.77, material_type=TRANSPARENT)
DIAMOND = Materials(spec=30, ior=2.41, material_type=TRANSPARENT)

# Materiales con textura
MOON = Materials(texture=Texture('../textures/earthDay.bmp'))

