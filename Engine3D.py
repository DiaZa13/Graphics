# Main
import gl
from numpy import sin, cos, pi

# Variables
width = 960
height = 700

render = gl.Render(width, height)
render.loadModel('Pallone/Ball OBJ.obj',  gl.V2(320, 320), gl.V2(width/3, height/2))

render.end('output2.bmp')
