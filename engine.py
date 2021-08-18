# Main
from libs.gl import Render, V3
from libs.obj import Texture
from libs.shaders import *

# Variables
width = 940
height = 800

render = Render(width, height)
render.active_shader = flat_shader
modelPosition = V3(-3, 3, -10)
render.loadModel('models/among_us.obj',
                 scale=V3(0.05, 0.05, 0.05),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

render.active_shader = gourad_shader
modelPosition = V3(3, 3, -10)
render.loadModel('models/among_us.obj',
                 scale=V3(0.05, 0.05, 0.05),
                 translate=modelPosition,
                 rotate=V3(0, 0, 0))

render.end('output.bmp')
