# Main
import gl

# Variables
width = 960
height = 540

render = gl.Render(width, height)
render.createViewport(100, 100, 10, 10)

render.drawPoint(-1, 1)
render.end('output.bmp')