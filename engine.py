# Main
from libs.gl import Render, V3
from libs.obj import Texture

# Variables
width = 960
height = 540

render = Render(width, height)
# render.CreateViewMatrix(V3(-1, 0, 0), V3(0, 30, 0))
modelPosition = V3(0, 0, -10)
render.lookAt(modelPosition, V3(-5, 5, 0))
model_texture = Texture('textures/face.bmp')
render.loadModel('models/face.obj', model_texture, V3(2, 2, 2), modelPosition, V3(0, 0, 0))
# render.loadModel('models/face.obj', model_texture, V3(3, 3, 3), V3(-3, 0, -5))
render.end('output.bmp')
