from raytracer import Raytracer, V3
from polygons import Sphere
from lighting import PointLight, AmbientLight, DirectionalLight
from materials import *
from rasterizador.obj import EnvMap

width = 1920
height = 1080


raytracer = Raytracer(width, height)
raytracer.envmap = EnvMap('../textures/park.bmp')

raytracer.ambientLight = AmbientLight(strength=0.1)
raytracer.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
raytracer.pointLights.append(PointLight(position=V3(1, 2, 1), intensity=0.5))

raytracer.scene.append(Sphere(V3(2, -3, -12), 1.5, METALLIC))
raytracer.scene.append(Sphere(V3(-0.5, -2.8, -7.5), 1.2, NEON_YELLOW))

raytracer.scene.append(Sphere(V3(5, -3, -15), 2, SKY))
raytracer.scene.append(Sphere(V3(15, -3, -20), 2, GRASS))

raytracer.scene.append(Sphere(V3(7, -3, -12), 1.3, SAPPHIRE))
raytracer.scene.append(Sphere(V3(-6, -2.8, -8), 1, ICE))

raytracer.render()
raytracer.end('output.bmp')
