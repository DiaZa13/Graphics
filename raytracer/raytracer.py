from gl import Raytracer, V3
from polygons import Sphere, PointLight
from materials import SKY, COPPER
from libs import zutils as zu

width = 256
height = 256


raytracer = Raytracer(width, height)

raytracer.pointLights.append(PointLight(position=V3(5, -7, 0)))
raytracer.pointLights.append(PointLight(position=V3(-10, 2, 0)))

raytracer.scene.append(Sphere(V3(0, 0, -14), radius=4, material=SKY))


raytracer.render()
raytracer.end('output.bmp')
