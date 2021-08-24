# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 480
height = 480

render = Render(width, height)
render.directional_light = (0, 0, -1)

render.active_shader = blue_shader
render.active_texture = Texture('textures/orange.bmp')
# render.normal_map = Texture('normals/orange')
modelPosition = V3(0, 0, -8)
render.loadModel('models/orange.obj',
                 scale=V3(0.04, 0.04, 0.04),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

render.end('output.bmp')
