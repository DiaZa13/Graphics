from gl import Raytracer, V3
from polygons import Sphere, PointLight
from materials import SKY, COPPER

width = 256
height = 256


raytracer = Raytracer(width, height)

raytracer.pointLight = PointLight(position=V3(-10, 2, 0))

raytracer.scene.append(Sphere(V3(0, 0, -14), radius=4, material=COPPER))


raytracer.render()
raytracer.end('output.bmp')
