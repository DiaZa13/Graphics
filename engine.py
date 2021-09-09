# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 1000
height = 667

render = Render(width, height)
# render.background = Texture('textures/background.bmp')
# render.clearBackground()
render.directional_light = V3(0, 0, -1)

# render.active_texture = Texture('textures/alien.bmp')
# model = 'models/alien.obj'
# render.active_shader = flat_shader
# modelPosition = V3(-9.3, 6, -15)
# render.loadModel(model,
#                  scale=V3(1.2, 1.2, 1.2),
#                  translate=modelPosition,
#                  rotate=V3(-90, -3, 45))

render.active_texture = Texture('textures/nave.bmp')
render.active_texture2 = Texture('textures/nave2.bmp')
render.glow_texture = Texture('textures/nave_glow.bmp')
render.spec_texture = Texture('textures/nave_specular.bmp')
model = 'models/nave.obj'
render.active_shader = space_unlit_shader
modelPosition = V3(-6, 2, -10)
render.loadModel(model,
                 scale=V3(0.05, 0.05, 0.05),
                 translate=modelPosition,
                 rotate=V3(0, 45, 0))


# render.directional_light = V3(-1, 1, -1)
# render.active_texture = Texture('textures/cow.bmp')
# model = 'models/cow.obj'
# render.active_shader = blinn_phong_reflection
# modelPosition = V3(-6.2, 0.3, -12)
# render.loadModel(model,
#                  scale=V3(1, 1, 1),
#                  translate=modelPosition,
#                  rotate=V3(-45, -30, 80))
#
#
# render.directional_light = V3(1, -1, 0)
# render.active_texture = Texture('textures/pig.bmp')
# model = 'models/pig.obj'
# render.active_shader = flat_shader
# modelPosition = V3(-6, -3.2, -12)
# render.loadModel(model,
#                  scale=V3(1, 1, 1),
#                  translate=modelPosition,
#                  rotate=V3(-90, -12, 75))


# render.directional_light = V3(0, 0, -1)
# render.active_texture = Texture('textures/tower1.bmp')
# render.active_texture = Texture('textures/tower2.bmp')
# model = 'models/tower.obj'
# render.active_shader = texture_interpol
# modelPosition = V3(5.3, -1.3, -8)
# render.loadModel(model,
#                  scale=V3(1, 1, 1),
#                  translate=modelPosition,
#                  rotate=V3(-90, 0, 0))


# render.directional_light = V3(1, -1, 0)
# render.active_texture = Texture('textures/hero.bmp')
# model = 'models/hero.obj'
# render.active_shader = toon_shader
# modelPosition = V3(2, -0.2, -8)
# render.loadModel(model,
#                  scale=V3(1.5, 1.5, 1.5),
#                  translate=modelPosition,
#                  rotate=V3(-105, 0, -90))

render.end('project.bmp')
