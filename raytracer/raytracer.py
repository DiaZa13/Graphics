from gl import Raytracer, V3
from libs.obj import Obj, Texture
from polygons import Sphere

width = 512
height = 512

raytrace = Raytracer(width, height)
raytrace.scene.append(Sphere(V3(0, 0, -10), radius=2))

raytrace.render()

raytrace.end('output.bmp')
