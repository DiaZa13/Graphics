# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 480
height = 480

render = Render(width, height)
render.directional_light = (-1, 0, 1)
# render.active_shader = flat_shader
# # render.active_texture = Texture('textures/orange.bmp')
# modelPosition = V3(-5, 0, -10)
# render.loadModel('models/orange.obj',
#                  scale=V3(0.04, 0.04, 0.04),
#                  translate=modelPosition,
#                  rotate=V3(0, 0, 0))
#
# render.active_shader = gourad_shader
# modelPosition = V3(0, 0, -10)
# render.loadModel('models/orange.obj',
#                  scale=V3(0.04, 0.04, 0.04),
#                  translate=modelPosition,
#                  rotate=V3(0, 0, 0))

render.active_shader = texture_interpol
render.active_texture = Texture('textures/face.bmp')
render.active_texture2 = Texture('textures/orange.bmp')
modelPosition = V3(0, 0, -10)
render.loadModel('models/orange.obj',
                 scale=V3(0.1, 0.1, 0.1),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

render.end('output.bmp')
