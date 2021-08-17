# Main
from libs.gl import Render, V3
from libs.obj import Texture

# Variables
width = 940
height = 800

render = Render(width, height)
model_texture = Texture('textures/face.bmp')
# -------Low angle
# modelPosition = V3(0, 5, -3)
# render.lookAt(modelPosition, V3(0, 6, 3))
# render.loadModel('models/face.obj', model_texture, V3(3, 3, 3),  modelPosition, V3(-35, 0, 0))

# High angle
# modelPosition = V3(0, 5, -3)
# render.lookAt(modelPosition, V3(0, 7, 5))
# render.loadModel('models/face.obj', model_texture, V3(3, 3, 3),  modelPosition, V3(20, 0, 0))

# Medium shot
# modelPosition = V3(0, 0, -3)
# render.lookAt(modelPosition, V3(0, 0, 0))
# render.loadModel('models/face.obj', model_texture, V3(2, 2, 2),  modelPosition, V3(0, -8, 0))

# Dutch angle
modelPosition = V3(2, 0, -5)
render.CreateViewMatrix(V3(0, 0, 0), V3(0, -20, 22))
render.loadModel('models/face.obj', model_texture, V3(2, 2, 2),  modelPosition, V3(0, 0, 0))

render.end('dutch_angle.bmp')
