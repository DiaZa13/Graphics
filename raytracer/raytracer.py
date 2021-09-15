from gl import Raytracer, V3
from polygons import Sphere, PointLight, AmbientLight, DirectionalLight
from materials import SKY, COPPER, GRASS, STONE
from libs import zutils as zu

width = 512
height = 512


raytracer = Raytracer(width, height)

# raytracer.pointLights.append(PointLight(position=V3(5, -7, 0)))
raytracer.ambientLight = AmbientLight(strength=0.1)
raytracer.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)
raytracer.pointLights.append(PointLight(position=V3(-10, 2, 0)))

raytracer.scene.append(Sphere(V3(0, 0, -8), radius=2, material=STONE))


raytracer.render()
raytracer.end('output.bmp')
