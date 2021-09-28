import libs.zmath as zm
import libs.zutils as zu
from libs.zutils import V3, WHITE

class Light(object):
    def __init__(self, light, intersect, light_direction):
        self.light = light
        self.intersect = intersect
        self.material = intersect.figure.material
        self.light_direction = light_direction

    def diffuse(self):
        intensity = max(0, zm.dot(self.intersect.normal, self.light_direction)) * self.light.intensity
        diffuse = [intensity * self.light.color[2] / 255,
                   intensity * self.light.color[1] / 255,
                   intensity * self.light.color[0] / 255]
        return diffuse

    def specular(self, camPosition):
        view_direction = zm.subtract(camPosition, self.intersect.point)
        view_direction = zm.normalize(view_direction)
        # Vector de la luz reflejada → R = 2 * (normal • light) * normal - light
        reflect = zu.reflection(self.intersect.normal, self.light_direction)
        intensity = self.light.intensity * pow((max(0, zm.dot(view_direction, reflect))), self.material.spec)
        specular = [intensity * self.light.color[2] / 255,
                    intensity * self.light.color[1] / 255,
                    intensity * self.light.color[0] / 255]
        return specular

class AmbientLight:
    def __init__(self, strength=0, color=WHITE):
        self.strength = strength
        self.color = color

    def getColor(self):
        ambient = [self.strength * self.color[2] / 255,
                   self.strength * self.color[1] / 255,
                   self.strength * self.color[0] / 255]
        return ambient

class DirectionalLight(object):
    def __init__(self, direction=V3(0, -1, 0), intensity=1, color=WHITE):
        self.direction = zm.normalize(direction)
        self.light_direction = [-i for i in self.direction]
        self.intensity = intensity
        self.color = color
        self.intersect = None
        self.specular = None
        self.shadow = None

    def shadowCalc(self, scene):
        shadow_intensity = 0
        shadow_intersect = scene.sceneIntersect(self.intersect.point, self.light_direction, self.intersect.figure)
        if shadow_intersect:
            shadow_intensity = 1

        return 1 - shadow_intensity

    def getColor(self, intersect, camPosition, scene):
        self.intersect = intersect
        self.shadow = self.shadowCalc(scene)
        light = Light(self, self.intersect, self.light_direction)
        diffuse = light.diffuse()
        specular = light.specular(camPosition)
        self.specular = zm.multiply(self.shadow, specular)
        directionalColor = zm.sum(diffuse, specular)
        directionalIntensity = zm.multiply(self.shadow, directionalColor)

        return directionalIntensity


class PointLight(object):
    # Es una luz con un punto de origen que se esparce a todas las direcciones
    # "genera" una cantidad infinita de rayos de luz en todas las direcciones
    def __init__(self, position=V3(0, 0, 0), intensity=1, color=WHITE):
        self.position = position
        self.intensity = intensity
        self.color = color
        self.intersect = None
        self.specular = None
        self.shadow = None

    def shadowCalc(self, scene):
        light_direction = zm.subtract(self.position, self.intersect.point)
        light_direction = zm.normalize(light_direction)
        shadow_intensity = 0
        shadow_intersect = scene.sceneIntersect(self.intersect.point, light_direction, self.intersect.figure)
        light_distance = zm.subtract(self.position, self.intersect.point)
        light_distance = zm.hypotenuse(light_distance)

        if shadow_intersect and shadow_intersect.distance < light_distance:
            shadow_intensity = 1

        return 1 - shadow_intensity

    def getColor(self, intersect, camPosition, scene):
        self.intersect = intersect
        self.shadow = self.shadowCalc(scene)
        light_direction = zm.subtract(self.position, self.intersect.point)
        light_direction = zm.normalize(light_direction)
        light = Light(self, intersect, light_direction)
        diffuse = light.diffuse()
        specular = light.specular(camPosition)
        self.specular = zm.multiply(self.shadow, specular)
        pointLightColor = zm.sum(diffuse, specular)
        pointLightIntensity = zm.multiply(self.shadow, pointLightColor)

        return pointLightIntensity



