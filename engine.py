# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 1000
height = 667

render = Render(width, height)
render.background = Texture('textures/background.bmp')
render.clearBackground()
render.directional_light = V3(0, 0, -1)

# render.active_texture = Texture('textures/tower1.bmp')
# model = 'models/tower.obj'
# render.active_shader = flat_shader
# modelPosition = V3(0, -1, -8)
# render.loadModel(model,
#                  scale=V3(1, 1, 1),
#                  translate=modelPosition,
#                  rotate=V3(-90, 0, 0))

render.active_texture = Texture('textures/nave.bmp')
model = 'models/nave.obj'
render.active_shader = space_shader
modelPosition = V3(-5.5, 3.5, -10)
render.loadModel(model,
                 scale=V3(3.5, 3.5, 3.5),
                 translate=modelPosition,
                 rotate=V3(-90, -5, 125))

render.directional_light = V3(1, -1, 0)
render.active_texture = Texture('textures/pig.bmp')
model = 'models/pig.obj'
render.active_shader = flat_shader
modelPosition = V3(-6, -1, -12)
render.loadModel(model,
                 scale=V3(1, 1, 1),
                 translate=modelPosition,
                 rotate=V3(-90, -12, 75))


render.directional_light = V3(-1, 1, -1)
render.active_texture = Texture('textures/cow.bmp')
model = 'models/cow.obj'
render.active_shader = blinn_phong_reflection
modelPosition = V3(-6, -3, -8)
render.loadModel(model,
                 scale=V3(1, 1, 1),
                 translate=modelPosition,
                 rotate=V3(-45, -10, 75))


render.directional_light = V3(0, 0, -1)
render.active_texture = Texture('textures/tower1.bmp')
render.active_texture = Texture('textures/tower2.bmp')
model = 'models/tower.obj'
render.active_shader = texture_interpol
modelPosition = V3(5.3, -1.3 , -8)
render.loadModel(model,
                 scale=V3(1, 1, 1),
                 translate=modelPosition,
                 rotate=V3(-90, 0, 0))

render.end('project.bmp')
