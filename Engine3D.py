# Main
from libs.gl import Render, V2

# Variables
width = 960
height = 700

render = Render(width, height)
render.drawTriangle(V2(10, 10), V2(190, 10), V2(100, 190))

render.end('output.bmp')
