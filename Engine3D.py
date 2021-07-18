# Main
import gl
from numpy import sin, cos, pi

# Variables
width = 960
height = 540

render = gl.Render(width, height)
# FIRST
# Esquina inferior izquierda
# render.viewport(width/2, height/2, 0, 0, gl.color(1, 1, 1))
# render.drawPoint_NDC(1, 1, gl.color(0.2, 0.2, 1))
# # Rombo
# for x in range(10,width//2, 10):
#     x0 = width/4
#     x1 = x
#     y0 = height/2 - 2
#     y1 = height/4
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0, 1, 0))
#
#     x0 = width / 4
#     x1 = x
#     y0 = 0
#     y1 = height / 4
#     # Bottom
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0, 1, 0))
#
# for x in range(10, height//2, 10):
#     x0 = 10
#     x1 = width/4
#     y0 = height/4
#     y1 = x
#
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0, 1, 0))
#
#     x0 = 470
#     x1 = width / 4
#     y0 = height / 4
#     y1 = x
#
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0, 1, 0))
#
# # Esquina inferior derecha
# render.viewport(width/2, height/2, width/2, 0, gl.color(0.5, 1, 0.5))
# render.drawPoint_NDC(-1, 1, gl.color(0.2, 0.2, 1))
# render.viewport(width/2 - 60, height/2 - 20, width/2 + 30, 10, gl.color(0.5, 1, 0.5))
# for x in range(0, width, 5):
#     x0 = width/2 + 10
#     x1 = width - 10
#     y0 = height/2 - 1
#     y1 = x
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.3, 0.3, 0.3))
#
#     x0 = width - 10
#     x1 = width / 2 + 10
#     y0 = height / 2 - 1
#     y1 = x
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.3, 0.3, 0.3))
#
#     x0 = width - 10
#     x1 = width / 2 + 10
#     y0 = 0
#     y1 = height/2 - x
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.3, 0.3, 0.3))
#
#     x0 = width / 2 + 10
#     x1 = width - 10
#     y0 = 0
#     y1 = height / 2 - x
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.3, 0.3, 0.3))
#
# # Esquina superior izquierda
# render.viewport(width/2, height/2, 0, height/2, gl.color(0.5, 0.5, 1))
# render.drawPoint_NDC(1, -1, gl.color(0, 0, 0))
# for x in range(20, 340):
#     degree = x * pi/180
#     x0 = width/4
#     x1 = (cos(degree) * 100) + width/4
#     y0 = 3 * height/4
#     y1 = (sin(degree) * 100) + (3/4 * height)
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.96, 0.72, 0))
#
# # Eye
# for x in range(0, 400):
#     degree = x * pi / 180
#     x0 = width / 4 + 25
#     x1 = (cos(degree) * 10) + width / 4 + 25
#     y0 = 3 * height / 4 + 50
#     y1 = (sin(degree) * 10) + (3 / 4 * height) + 50
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0, 0, 0))
#
# # Esquina superior derecha
# render.viewport(width/2, height/2, width/2, height/2, gl.color(0.5, 0.5, 0.5))
# render.drawPoint_NDC(-1, -1, gl.color(0.2, 0.2, 1))
# for x in range(0, 500):
#     degree = x * pi / 180
#     x0 = (3 / 4 * width) + 20
#     x1 = (cos(degree) * 40) + (3 / 4 * width) + 20
#     y0 = (3/4 * height) + 12
#     y1 = (sin(degree) * 40) + (3/4 * height) + 12
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(1, 0, 0))
#
#     x0 = (3 / 4 * width) - 43
#     x1 = (cos(degree) * 40) + (3 / 4 * width) - 43
#     y0 = (3 / 4 * height) + 12
#     y1 = (sin(degree) * 40) + (3 / 4 * height) + 12
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(1, 0, 0))
#
# for x in range(158, width//4 + 60):
#     x0 = 3/4 * width - 10
#     x1 = x + width/2
#     y0 = height/2 + 60
#     y1 = 3/4 * height
#     # Bottom
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(1, 0, 0))

# SECOND
render.viewport(width/2 + 10, height, width/4, 0, gl.color(0, 0, 0))

for x in range(0, width, 20):
    render.drawLine(gl.V2(0 + width/4 ,x), gl.V2(x + width/4,height))
    render.drawLine(gl.V2(x + width/4 - 53, 0), gl.V2(height + width/4 - 53, x))

for x in range(0, 400,2):
    degree = x * pi / 180
    x0 = (cos(degree) * 40) + (width/2)
    x1 = (cos(degree) * 41) + (width/2)
    y0 = (sin(degree) * 40) + (height/2)
    y1 = (sin(degree) * 41) + (height/2)
    # Up
    render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.23, 0.51, 0.74))

    x0 = (cos(degree) * 40) + (width/2)
    x1 = (cos(degree) * 91) + (width/2)
    y0 = (sin(degree) * 40) + (height/2)
    y1 = (sin(degree) * 91) + (height/2)
    # Up
    render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.23, 0.51, 0.74))

for x in range(0,400, 5):
    degree = x * pi / 180
    x0 = (cos(degree) * 50) + (width / 2)
    x1 = (cos(degree) * 91) + (width / 2)
    y0 = (sin(degree) * 50) + (height / 2)
    y1 = (sin(degree) * 91) + (height / 2)

    render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.18, 0.34, 0.17))

    x0 = (cos(degree) * 40) + (width / 2)
    x1 = (cos(degree) * 91) + (width / 2)
    y0 = (sin(degree) * 40) + (height / 2)
    y1 = (sin(degree) * 91) + (height / 2)

    render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.18, 0.34, 0.17))



# EXTRA
# for x in range(0, 400):
#     degree = x * pi / 180
#     x0 = (cos(degree) * 100) + (3/4 * width)
#     x1 = (cos(degree) * 250) + (2/3 * width)
#     y0 = (sin(degree) * 100) + (3/4 * height)
#     y1 = (sin(degree) * 250) + (2/3 * height)
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.31, 0.71, 0.89))
#
# for x in range(0, 400):
#     degree = x * pi / 180
#     x0 = (cos(degree) * 100) + (3/4 * width)
#     x1 = (3/4 * width) - 100
#     y0 = (sin(degree) * 100) + (3/4 * height)
#     y1 = (3/4 * height) - 100
#     # Up
#     render.drawLine(gl.V2(x0, y0), gl.V2(x1, y1), gl.color(0.31, 0.71, 0.89))
render.end('output2.bmp')
