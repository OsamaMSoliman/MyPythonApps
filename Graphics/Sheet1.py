from Graphics.Circle import *
from Graphics.StraightLine import *

if __name__ == "__main__":
    print("Q1:- straight_line((2, 1), (8, 6)): ")
    print_points(straight_line((2, 1), (8, 6)))

    print()

    print("Q2:- straight_line((3, 4), (8, 12)): ")
    print_points(raster((3, 4), (8, 12)))
    print("Q2:- straight_line((8, 12), (8, 10)): ")
    print_points(raster((8, 12), (8, 10)))
    print("Q2:- straight_line((8, 10), (16, 13)): ")
    print_points(raster((8, 10), (16, 13)))
    print("Q2:- straight_line((16, 13), (19, 10)): ")
    print_points(raster((16, 13), (19, 10)))
    print("Q2:- straight_line((19, 10), (20, 4)): ")
    print_points(raster((19, 10), (20, 4)))
    print("Q2:- straight_line((20, 4), (16, 10)): ")
    print_points(raster((20, 4), (16, 10)))
    print("Q2:- straight_line((16, 10), (3, 4)): ")
    print_points(raster((16, 10), (3, 4)))

    print()

    print("Q3:- Circle: radius= 9, center =100, 100 : ")
    print_points_circle(circle(radius=9, center=(100, 100)))

    print()

    print("Q4:- D (6, 6), C (8, 10): ")
    print_points(raster((6, 6), (8, 10)))
    print("Q4:- F (6, 2), E (15, 16): ")
    print_points(raster((6, 2), (15, 16)))
    print("Q4:- H (14, 3), G (16, 9): ")
    print_points(raster((14, 3), (16, 9)))

    print()

    print("Q5:- P 1 (0, 0) , P 2 (0, 9) : ")
    print_points(raster((0, 0), (0, 9)))
    print("Q5:- P 1 (0, 0) , P 3 (6, 6) : ")
    print_points(raster((0, 0), (6, 6)))
    print("Q5:- radius= 9, center =0,0 : ")
    print_points_circle(circle(radius=9, center=(0, 0)))

    print()

    print("Q6:- Circle: radius= 10, center =2, 6 : ")
    print_points_circle(circle(radius=10, center=(2, 6)))