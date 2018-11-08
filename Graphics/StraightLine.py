# this code takes 2 points and calc the points of the straight line in between
# NOTE this uses the midPoint method ( the slope must be less than 1 )


def straight_line(pStart, pEnd):
    points = []
    # calc the slope to check if the midPoint method is valid
    dy = pEnd[1] - pStart[1]
    dx = pEnd[0] - pStart[0]
    m = dy / dx
    if m > 1 or m < 0:
        return
    # print the 1st point
    points.append(pStart)
    # check if the straight line is parallel to any of the Axis
    if m == 1:
        pass
    elif m == 0:
        pass
    # else follow the midPoint method
    else:
        # get d0 1st
        d = dy - dx / 2
        while points[-1][1] < pEnd[1] or points[-1][0] < pEnd[0]:
            # if NorthEast (NE)
            if d > 0:
                pNew = (points[-1][0] + 1, points[-1][1] + 1)
                d += dy - dx
            # else East (E)
            else:
                pNew = (points[-1][0] + 1, points[-1][1])
                d += dy
            points.append(pNew)
    return points


def raster(pStart, pEnd):
    points = []
    dy = pEnd[1] - pStart[1]
    dx = pEnd[0] - pStart[0]
    try:
        m = dy / dx
    except ZeroDivisionError:
        m = None
    points.append(pStart)
    if m is None:
        if dy > 0:
            while points[-1][1] < pEnd[1]:
                points.append((pStart[0], points[-1][1] + 1))
        else:
            while points[-1][1] > pEnd[1]:
                points.append((pStart[0], points[-1][1] - 1))
    elif m == 0:
        if dx > 0:
            while points[-1][0] < pEnd[0]:
                points.append((points[-1][0] + 1, pStart[1]))
        else:
            while points[-1][0] > pEnd[0]:
                points.append((points[-1][0] - 1, pStart[1]))
    elif m > 1 or m == 1:
        if dy > 0:
            while points[-1][1] < pEnd[1]:
                points.append(((points[-1][0] + (1 / m)), points[-1][1] + 1))
        else:
            while points[-1][1] > pEnd[1]:
                points.append(((points[-1][0] - (1 / m)), points[-1][1] - 1))
    elif 1 > m > 0:
        if dx > 0:
            while points[-1][0] < pEnd[0]:
                points.append((points[-1][0] + 1, (points[-1][1] + m)))
        else:
            while points[-1][0] > pEnd[0]:
                points.append((points[-1][0] - 1, (points[-1][1] - m)))
    elif 0 > m > -1:
        if dx > 0:
            while points[-1][0] > pEnd[0]:
                points.append((points[-1][0] + 1, (points[-1][1] + m)))
        else:
            while points[-1][0] < pEnd[0]:
                points.append((points[-1][0] - 1, (points[-1][1] - m)))
    elif m < -1 or m == -1:
        if dy > 0:
            while points[-1][1] > pEnd[1]:
                points.append(((points[-1][0] + (1 / m)), points[-1][1] - 1))
        else:
            while points[-1][1] < pEnd[1]:
                points.append(((points[-1][0] - (1 / m)), points[-1][1] + 1))
    return points


def print_points(points):
    if points is not None:
        for p in points:
            print((int(p[0]), int(p[1])))


if __name__ == "__main__":
    # print("Q1:- straight_line((2, 1), (8, 6)): ")
    # print_points(straight_line((2, 1), (8, 6)))
    #
    # print("Q2:- straight_line((3, 4), (8, 12)): ")
    # print_points(raster((3, 4), (8, 12)))

    # print("Q2:- straight_line((16, 13), (19, 10)): ")
    # print_points(raster((16, 13), (19, 10)))

    # print("Q2:- straight_line((8, 12), (8, 10)): ")
    # print_points(raster((8, 12), (8, 10)))

    print("Q2:- straight_line((16, 10), (3, 4)): ")
    print_points(raster((16, 10), (3, 4)))
