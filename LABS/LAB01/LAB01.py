import gl

# Variables
width = 960
height = 540

render = gl.Render(width, height)

# Poligonos
pol1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410),
        (193, 383)]
pol2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
pol3 = [(377, 249), (411, 197), (436, 249)]
pol4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179),
        (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]
pol5 = [(682, 175), (708, 120), (735, 148), (739, 170)]


# Draw polygon
def drawPolygon(polygon):
    limit = len(polygon)
    for v in range(limit):
        render.drawLine(gl.V2(polygon[v][0], polygon[v][1]),
                        gl.V2(polygon[(v + 1) % limit][0], polygon[(v + 1) % limit][1]))


render.drawColor(243, 202, 64)
drawPolygon(pol1)
render.drawColor(242, 165, 65)
drawPolygon(pol2)
render.drawColor(240, 138, 75)
drawPolygon(pol3)
render.drawColor(87, 117, 144)
drawPolygon(pol4)
render.drawColor(0, 0, 0)
drawPolygon(pol5)

render.drawColor(243, 202, 64)
render.filling(pol1, 'e')
render.drawColor(242, 165, 65)
render.filling(pol2)
render.drawColor(240, 138, 75)
render.filling(pol3)
render.drawColor(87, 117, 144)
render.filling(pol4, 't')
render.drawColor(0, 0, 0)
render.filling(pol5)

render.end('filling.bmp')
