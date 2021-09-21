from gl import Raytracer, V3
from polygons import Sphere, PointLight, AmbientLight, DirectionalLight
from materials import SKY, COPPER, GRASS, STONE
from libs import zutils as zu

width = 128
height = 128


raytracer = Raytracer(width, height)


raytracer.ambientLight = AmbientLight(strength=0.1)
raytracer.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
raytracer.pointLights.append(PointLight(position=V3(0, 2, 0)))
# raytracer.pointLights.append(PointLight(position=V3(5, -7, 0)))

raytracer.scene.append(Sphere(V3(0, 0, -8), 2, GRASS))
raytracer.scene.append(Sphere(V3(-1, 1, -5), 0.5, SKY))
raytracer.scene.append(Sphere(V3(0.5, 0.5, -5), 0.5, COPPER))



raytracer.render()
raytracer.end('output.bmp')
