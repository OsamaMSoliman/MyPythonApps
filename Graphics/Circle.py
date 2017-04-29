# this code takes the center point of the circle and the radius ,, calc the points of the circle in line in between
# NOTE this uses the midPoint method ( the slope must be less than 1 )


def circle(radius, center):
    # the 1st point already known
    x = 0
    y = radius
    # list of points
    points_origin = [(x, y)]
    # get d0 1st
    d = 1.25 - radius
    # while the X of the last point is less than it's Y
    # while points[-1][0] < points[-1][1]:
    while x < y:
        # if SouthEast (SE)
        if d > 0:
            d += 2 * x - 2 * y + 5
            x += 1
            y -= 1
        # else East (E)
        else:
            d += 2 * x + 3
            x += 1
        points_origin.append((x, y))
    # this list contains the right points aground the center
    points_center = []
    if center != (0, 0):
        for point in points_origin:
            points_center.append((point[0] + center[0], point[1] + center[1]))
    # this list contains ALL the right points aground the center that form the whole circle
    points_final = []
    for point in points_center:
        points_final.extend(point_permutations(point))
    return points_origin, points_center, points_final


def point_permutations(point):
    x = point[0]
    y = point[1]
    permutations = [
        (x, y),
        (-1 * x, -1 * y),
        (x, -1 * y),
        (-1 * x, y),
        (y, x),
        (-1 * y, -1 * x),
        (y, -1 * x),
        (-1 * y, x)
    ]
    return permutations


if __name__ == "__main__":
    points = circle(7, (3, 6))
    for p in points:
        print(p)
