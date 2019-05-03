import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    a = calculate_ambient(ambient, areflect)
    #a = [0, 0, 0]
    b = calculate_diffuse(light, dreflect, normal)
    #b = [0, 0, 0]
    c = calculate_specular(light, sreflect, view, normal)
    #c = [0, 0, 0]
    d =[int(a[0]) + int(b[0]) + int(c[0]),
        int(a[1]) + int(b[1]) + int(c[1]),
        int(a[2]) + int(b[2]) + int(c[2])]
    limit_color(d)
    return d

def calculate_ambient(alight, areflect):
    ret = [0, 0, 0]
    for i in range(0,3):
        ret[i] = alight[i] * areflect[i]
    return ret
    

def calculate_diffuse(light, dreflect, normal):
    colors = [light[COLOR][0], light[COLOR][1], light[COLOR][2]]
    normalize(normal)
    constant = dot_product(normal, light[LOCATION])
    for i in range(0, 3):
        colors[i] *= constant * dreflect[i]
        if colors[i] < 0:
            colors[i] = 0
    return colors

def calculate_specular(light, sreflect, view, normal):
    colors = [light[COLOR][0], light[COLOR][1], light[COLOR][2]]
    normalize(normal)
    cons = dot_product(normal, light[LOCATION])
    ncpy = normal[:]
    for i in range(0, 3):
        ncpy[i] *= 2 * cons
        ncpy[i] -= light[LOCATION][i]
    for i in range(0, 3):
        colors[i] *= (sreflect[i] * dot_product(ncpy, view)) ** 3
        colors[i] = colors[i]
        if colors[i] < 0:
            colors[i] = 0
    return colors

def limit_color(color):
    for i in range(0,3):
        if color[i] > 255:
            color[i] = 255

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
