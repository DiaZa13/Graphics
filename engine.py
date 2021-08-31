# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 960
height = 540

render = Render(width, height)
render.active_texture = Texture('textures/face.bmp')
model = 'models/face.obj'

render.directional_light = V3(0, 0, -1)

# Blue shader
render.active_shader = blue_shader
modelPosition = V3(5, 2, -8)
render.loadModel(model,
                 scale=V3(2, 2, 2),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

render.end('face_shaders.bmp')
