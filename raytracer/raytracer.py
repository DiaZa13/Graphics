from gl import Raytracer, V3
from libs.obj import Obj, Texture
from libs.zutils import _color
from polygons import Sphere, Materials

width = 512
height = 512

snow = Materials(_color(219 / 255, 213 / 255, 234 / 255))
snow_light = Materials(_color(214 / 255, 208 / 255, 232 / 255))
black = Materials(_color(0, 0, 0))
red = Materials(_color(1, 0, 0))
carrot = Materials(_color(245 / 255, 111 / 255, 64 / 255))
white = Materials(_color(1, 1, 1))
gray = Materials(_color(93 / 255, 83 / 255, 74 / 255))

raytrace = Raytracer(width, height)
# Cuerpo
raytrace.scene.append(Sphere(V3(0, 3.5, -10), radius=1.5, material=snow_light))
raytrace.scene.append(Sphere(V3(0, 1, -15), radius=3, material=snow))
raytrace.scene.append(Sphere(V3(0, -2.5, -10), radius=2.5, material=snow_light))
# Botones
raytrace.scene.append(Sphere(V3(0, 1.2, -8), radius=0.25, material=black))
raytrace.scene.append(Sphere(V3(0, 0, -8), radius=0.3, material=black))
raytrace.scene.append(Sphere(V3(0, -1.5, -8), radius=0.5, material=black))
# Ojos
raytrace.scene.append(Sphere(V3(-0.4, 3.5, -8), radius=0.2, material=white))
raytrace.scene.append(Sphere(V3(0.4, 3.5, -8), radius=0.2, material=white))
raytrace.scene.append(Sphere(V3(-0.31, 3.08, -7), radius=0.1, material=black))
raytrace.scene.append(Sphere(V3(0.37, 3.08, -7), radius=0.1, material=black))
# Nariz
raytrace.scene.append(Sphere(V3(0, 3, -8), radius=0.25, material=carrot))
# Boca
raytrace.scene.append(Sphere(V3(-0.55, 2.5, -8), radius=0.1, material=gray))
raytrace.scene.append(Sphere(V3(-0.20, 2.3, -8), radius=0.1, material=gray))
raytrace.scene.append(Sphere(V3(0.20, 2.3, -8), radius=0.1, material=gray))
raytrace.scene.append(Sphere(V3(0.555, 2.5, -8), radius=0.1, material=gray))


raytrace.render()

raytrace.end('output.bmp')
