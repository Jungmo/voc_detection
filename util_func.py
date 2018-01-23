import numpy as np

def points_in_approx(approx):
    a = approx[0]
    b = approx[1]
    c = approx[2]
    d = approx[3]

    ax = a[0][0]
    ay = a[0][1]

    bx = b[0][0]
    by = b[0][1]

    cx = c[0][0]
    cy = c[0][1]

    dx = d[0][0]
    dy = d[0][1]

    minx = min(ax, bx, cx, dx)
    maxx = max(ax, bx, cx, dx)

    miny = min(ay, by, cy, dy)
    maxy = max(ay, by, cy, dy)

    return (minx, miny), (maxx, maxy)

def length_point_to_point(point_start, point_end):
    return ((point_end[0] - point_start[0])**2 + (point_end[1]-point_start[1])**2)**0.5

def is_big_or_small(approx):

    point_start, point_end = points_in_approx(approx)

    # big
    if length_point_to_point(point_start,point_end) > 400:
        print "big"
        return True
    # small
    elif length_point_to_point(point_start,point_end) < 20:
        print "small"
        return True
    else :
        return False

def extract_near_color_average(image, point_start, point_end, x,y):
    pixels = []
    radius = 4
    s = (point_start[0]+x-radius, point_start[1]+y-radius)

    for width in range(radius*2+1):
        for height in range(radius*2+1):
            pixels.append(image[s[1]+width][s[0]+height])

    return np.average(pixels,axis=0)


def extract_twenty_five_colors(image, approx):
    point_start, point_end = points_in_approx(approx)
    width = point_end[0]-point_start[0]
    height = point_end[1] - point_start[1]
    center = []
    pixels = []
    for x in range(width/6-1,width-width/6,width/6):
        for y in range(height/6-1,height-height/6,height/6):
            center.append((x,y))
    count = 1
    for x,y in center:
        #print count, extract_near_color_average(image, point_start,point_end,x,y)
        pixels.append(extract_near_color_average(image, point_start,point_end,x,y))
        count +=1

    return pixels

