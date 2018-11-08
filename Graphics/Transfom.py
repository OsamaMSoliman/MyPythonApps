import math
import numpy


# return a point in any dimension
def P(*args):
    matrix = []
    for arg in args:
        matrix.append([arg])
    matrix.append([1])
    return numpy.matrix(matrix)


# return a translation matrix in any dimension
def T(*args):
    size = len(args)
    matrix = numpy.identity(size + 1)
    for i in range(size):
        matrix[i][size] = args[i]
    return matrix


# return a scale matrix in dimension = size
def S(size, *args):
    if size == len(args):
        matrix = numpy.identity(size + 1)
        for i in range(size):
            matrix[i][i] = args[i]
        return matrix


# return a rotation matrix in a 2 dimension
def R2D(angle):
    print("numpy.cos: ", numpy.cos(numpy.deg2rad(angle)), "\nnumpy.sin: ", numpy.sin(numpy.deg2rad(angle)))
    print("math.cos: ", math.cos(math.radians(angle)), "\nmath.sin: ", math.sin(math.radians(angle)))
    cos = numpy.cos(numpy.deg2rad(angle))
    sin = numpy.sin(numpy.deg2rad(angle))
    matrix = [[cos, -1 * sin, 0], [sin, cos, 0], [0, 0, 1]]
    return numpy.matrix(matrix)


if __name__ == "__main__":
    s = S(2, 2, 3)
    t = T(5, 4)
    st = numpy.dot(s, t)
    ts = numpy.dot(t, s)
    print(ts)
