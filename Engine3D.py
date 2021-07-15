# Main
import gl
from numpy import sin, cos

# Variables
width = 960
height = 540

render = gl.Render(width, height)
render.viewport(500, 200, 30, 180, gl.color(1,1,1))

render.drawPoint_NDC(1, 1, gl.color(0.2, 0.2, 1))
render.drawLine(gl.V2(2, 5), gl.V2(900, 420), gl.color(1,0,0))

for x in range(width):
    x0 = x
    x1 = x + 1

    y0 = sin(x0 * 0.1) * 50 + height/2
    y1 = sin(x1 * 0.1) * 50 + height/2

    render.drawLine(gl.V2(int(x0), int(y0)), gl.V2(int(x1), int(y1)), gl.color(0.3,0.5,0.6))

render.end('output.bmp')
