# Main
from libs.gl import Render, V2

# Variables
width = 960
height = 700

render = Render(width, height)
render.drawTriangle(V2(10, 190), V2(190, 190), V2(100, 10))

render.end('output.bmp')
