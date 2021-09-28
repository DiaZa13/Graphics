from raytracer import Raytracer, V3
from polygons import Sphere
from lighting import PointLight, AmbientLight, DirectionalLight
from materials import *
from rasterizador.obj import EnvMap

width = 1024
height = 1024


raytracer = Raytracer(width, height)
raytracer.envmap = EnvMap('../textures/parking.bmp')

raytracer.ambientLight = AmbientLight(strength=0.1)
raytracer.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
raytracer.pointLights.append(PointLight(position=V3(0, 2, 0), intensity=0.5))
# raytracer.pointLights.append(PointLight(position=V3(5, -7, 0)))

raytracer.scene.append(Sphere(V3(0, 0, -8), 2, STONE))
raytracer.scene.append(Sphere(V3(-1, 1, -5), 0.5, MIRROR))
raytracer.scene.append(Sphere(V3(0.5, 0.5, -5), 0.5, GOLD))

raytracer.render()
raytracer.end('output.bmp')
