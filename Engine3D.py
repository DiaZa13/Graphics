# Main
from libs.gl import Render, V2

# Variables
width = 940
height = 700

render = Render(width, height)
# render.drawTriangle(V2(180, 50), V2(150, 1), V2(70, 180))

render.loadModel('models/ball.obj', V2(320, 320), V2(width/2, height/2))
render.end('output.bmp')
