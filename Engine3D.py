# Main
from libs.gl import Render, V2

# Variables
width = 200
height = 200

render = Render(width, height)
render.drawTriangle(V2(180, 50), V2(150, 1), V2(70, 180))

render.end('output.bmp')
