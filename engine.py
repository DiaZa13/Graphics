# Main
from libs.gl import Render, V2, V3

# Variables
width = 940
height = 700

render = Render(width, height)
# render.drawTriangle(V2(180, 50), V2(150, 1), V2(70, 180))
# render.drawTriangle_bc(V2(10, 10), V2(190, 10), V2(100, 190))
render.loadModel('models/face.obj', V3(300, 300, 300), V3(width/2, height/2, 0))
render.end('output.bmp')
