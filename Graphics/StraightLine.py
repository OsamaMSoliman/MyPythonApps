# this code takes 2 points and calc the points of the straight line in between
# NOTE this uses the midPoint method ( the slope must be less than 1 )

# the 2 points
pStart = (3, 5)
pEnd = (8, 8)
points = []


def main():
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
    for p in points:
        print(p)


if __name__ == "__main__":
    main()
