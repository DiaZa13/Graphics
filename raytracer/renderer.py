from raytracer import Raytracer, V3
from polygons import Sphere, Plane, AABB
from lighting import PointLight, AmbientLight, DirectionalLight
from materials import *
from rasterizador.obj import EnvMap

width = 256
height = 256

raytracer = Raytracer(width, height)
raytracer.envmap = EnvMap('../textures/park.bmp')

raytracer.ambientLight = AmbientLight(strength=0.1)
raytracer.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
raytracer.pointLights.append(PointLight(position=V3(0, 2, 0), intensity=0.5))

raytracer.scene.append(Sphere(V3(-2, 0, -8), 1.5, MOON))

raytracer.scene.append(AABB(V3(2, 0, -8), V3(2, 2, 2), MOON))

raytracer.render()
raytracer.end('output.bmp')
