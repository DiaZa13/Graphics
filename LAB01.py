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
# Draw polygon
def drawPolygon(polygon):
    limit = len(polygon)
    for v in range(limit):
        render.drawLine(gl.V2(polygon[v][0], polygon[v][1]), gl.V2(polygon[(v + 1) % limit][0], polygon[(v + 1) % limit][1]))


render.drawColor(0.5,0.8,0.8)
drawPolygon(pol1)
drawPolygon(pol2)
drawPolygon(pol3)

render.drawColor(1,1,1)
def filling(polygon):
    limit = len(polygon)
    x_coordinates = []
    y_coordinates = []
    for v in polygon:
        x_coordinates.append(v[0])
        y_coordinates.append(v[1])

    y_max = max(y_coordinates)
    y_min = min(y_coordinates)

    slopes = []
    for v in range(limit):
        x0 = polygon[v][0]
        y0 = polygon[v][1]
        x1 = polygon[(v + 1) % limit][0]
        y1 = polygon[(v + 1) % limit][1]

        m = (y1 - y0) / (x1 - x0)
        if m != 0:
            slopes.append((m, x1, y1))

    for a in range(y_min, y_max + 1):
        x1 = ((a - slopes[0][2])/slopes[0][0]) + slopes[0][1]
        x2 = ((a - slopes[1][2])/slopes[1][0]) + slopes[1][1]

        if x1 > x2:
            x1, x2 = x2, x1
        render.drawLine(gl.V2(x1, a), gl.V2(x2, a))

filling(pol2)
filling(pol3)
filling(pol1)

render.end('filling.bmp')