from raytracer import Raytracer, V3
from polygons import Sphere, Plane, AABB
from lighting import PointLight, AmbientLight, DirectionalLight
from materials import *
from rasterizador.obj import EnvMap

width = 512
height = 512


raytracer = Raytracer(width, height)
raytracer.envmap = EnvMap('../textures/parking.bmp')

raytracer.ambientLight = AmbientLight(strength=0.1)
raytracer.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
raytracer.pointLights.append(PointLight(position=V3(0, 2, 0), intensity=0.5))
# raytracer.pointLights.append(PointLight(position=V3(5, -7, 0)))

raytracer.scene.append(AABB(V3(-3, -3, -8), V3(3, 3, 3), STONE))

raytracer.render()
raytracer.end('output.bmp')
