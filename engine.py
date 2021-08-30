# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 960
height = 540

render = Render(width, height)
render.directional_light = (1, 1, 1)
# render.camPosition = V3(5, 3, 0)


render.active_shader = blinn_phong_reflection
render.active_texture = Texture('textures/orange.bmp')
render.active_texture2 = Texture('textures/noise.bmp')
modelPosition = V3(-2, 0, -8)
render.lookAt(modelPosition)
render.loadModel('models/orange.obj',
                 scale=V3(0.05, 0.05, 0.05),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

render.active_shader = lava_shader
render.active_texture = Texture('textures/orange.bmp')
render.active_texture2 = Texture('textures/noise.bmp')
modelPosition = V3(2, 0, -8)
render.lookAt(modelPosition)
render.loadModel('models/orange.obj',
                 scale=V3(0.05, 0.05, 0.05),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))




render.end('output.bmp')
