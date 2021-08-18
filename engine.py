# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 940
height = 540

render = Render(width, height)
render.active_shader = flat_shader
# render.active_texture = Texture('textures/orange.bmp')
modelPosition = V3(-3, 0, -10)
render.loadModel('models/orange.obj',
                 scale=V3(0.1, 0.1, 0.1),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

# render.active_shader = gourad_shader
# modelPosition = V3(3, 0, -10)
# render.loadModel('models/.obj',
#                  scale=V3(0.1, 0.1, 0.1),
#                  translate=modelPosition,
#                  rotate=V3(0, 0, 0))

render.end('output.bmp')
