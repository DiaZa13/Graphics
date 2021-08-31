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

# Space shader
render.active_shader = space_shader
modelPosition = V3(0, -2, -8)
render.loadModel(model,
                 scale=V3(2, 2, 2),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

# Lava shader
render.active_shader = lava_shader
render.active_texture2 = Texture('textures/noise.bmp')
modelPosition = V3(-5, -2, -8)
render.loadModel(model,
                 scale=V3(2, 2, 2),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

# Pattern shader
render.directional_light = (0, 1, -1)
render.active_shader = pattern
modelPosition = V3(5, -2, -8)
render.loadModel(model,
                 scale=V3(2, 2, 2),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

# Static shader
render.active_shader = static
modelPosition = V3(-5, 2, -8)
render.loadModel(model,
                 scale=V3(2, 2, 2),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

# Bling phong shader
render.camPosition = V3(5, 3, 0)
render.directional_light = (-1, 1, 1)
render.active_shader = blinn_phong_reflection
modelPosition = V3(0, 2, -8)
render.loadModel(model,
                 scale=V3(2, 2, 2),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

render.end('face_shaders.bmp')
