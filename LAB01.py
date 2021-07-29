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


render.drawColor(255, 174, 3)
drawPolygon(pol1)
render.drawColor(230, 127, 13)
drawPolygon(pol2)
render.drawColor(254, 78, 0)
drawPolygon(pol3)
render.drawColor(233, 25, 15)
drawPolygon(pol4)
render.drawColor(0, 0, 0)
drawPolygon(pol5)

render.drawColor(1, 1, 1)


def filling(polygon, clase=None):
    limit = len(polygon)
    x_coordinates = []
    y_coordinates = []
    slopes = []
    drawX = []
    for v in polygon:
        x_coordinates.append(v[0])
        y_coordinates.append(v[1])

    y_max = max(y_coordinates)
    y_min = min(y_coordinates)

    for v in range(limit):
        x0 = polygon[v][0]
        y0 = polygon[v][1]
        x1 = polygon[(v + 1) % limit][0]
        y1 = polygon[(v + 1) % limit][1]

        m = (y1 - y0) / (x1 - x0)

        slopes.append(m)

    for y in range(y_min, y_max):

        for v in range(limit):
            a = polygon[v][1]
            b = polygon[(v + 1) % limit][1]
            x = polygon[v][0]
            if (a <= y < b) or (b <= y < a):
                x = round(((y - a) / slopes[v]) + x)
                drawX.append(x)

        render.drawLine(gl.V2(drawX[(len(drawX) - 2)], y), gl.V2(drawX[len(drawX) - 1], y))
        if clase == 'e':
            if y_min <= y < 345:
                render.drawLine(gl.V2(drawX[(len(drawX) - 4)], y), gl.V2(drawX[len(drawX) - 3], y))
                render.drawLine(gl.V2(drawX[(len(drawX) - 2)], y), gl.V2(drawX[len(drawX) - 1], y))
        elif clase == 't':
            if 144 <= y < 177:
                render.drawLine(gl.V2(drawX[(len(drawX) - 4)], y), gl.V2(drawX[len(drawX) - 3], y))
                render.drawLine(gl.V2(drawX[(len(drawX) - 2)], y), gl.V2(drawX[len(drawX) - 1], y), gl.color(0, 0, 0))
            elif 177 <= y < 180:
                render.drawLine(gl.V2(drawX[(len(drawX) - 4)], y), gl.V2(drawX[len(drawX) - 3], y))

render.drawColor(255, 174, 3)
filling(pol1, 'e')
render.drawColor(230, 127, 13)
filling(pol2)
render.drawColor(254, 78, 0)
filling(pol3)
render.drawColor(233, 25, 15)
filling(pol4, 't')
render.drawColor(0, 0, 0)
filling(pol5)

render.end('filling.bmp')
