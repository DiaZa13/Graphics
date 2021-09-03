# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 960
height = 540

render = Render(width, height)
render.active_texture = Texture('textures/8.bmp')
model = 'models/sol.obj'

render.directional_light = V3(0, 0, -1)

# Blue shader
render.active_shader = flat_shader
modelPosition = V3(0, 0, -8)
render.loadModel(model,
                 scale=V3(1, 1, 1),
                 translate=modelPosition,
                 rotate=V3(0, 45, 0))

render.end('project.bmp')
