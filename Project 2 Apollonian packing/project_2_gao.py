import math
import cmath
from PIL import Image, ImageDraw


# turn x,y to pixel coordinates, input x,y, output coordinate tuple
def pxy(x, y):
    px = (x-xmin)/deltax
    py = (y-ymin)/deltay
    return (px, py)


# input 2 circles, output boolean, if mutually tangent return True
def two_tangent(a,b):
    eps = 0.000001
    if abs(abs(a[0]-b[0]) - (abs(a[1])+abs(b[1]))) < eps or abs(
            abs(a[0]-b[0]) - abs((abs(a[1])-abs(b[1])))) < eps:
        return True
    else:
        return False


# input 3 circles, output boolean, if mutually tangent return True
def three_tangent(a,b,c):
    return two_tangent(a, b) and two_tangent(a, c) and two_tangent(c, b)


# input 4 circles, output boolean, if mutually tangent return True
def four_tangent(a, b, c, d):
    return three_tangent(a,b,c) and three_tangent(a,b,d) and \
           three_tangent(d,b,c)


# input 3 mutually tangent circles, output a new circle that's mutually
# tangent to three input circles
# might return None because in tw0_tangent function we have a
# tolerance threshold of 0.000001, so it might be tangent but the
# circle might get very small as we increase iteration n.
def fourth_circle(a, b, c):
    # k1,k2,k3 are curvatures, given by 1/r, where the outer circle 
    # has negative r, which means externally tangent.
    k1 = 1.0 /a[1]
    k2 = 1.0 /b[1]
    k3 = 1.0 /c[1]
    # calculating curvature of the new circle
    temp0 = 2.0 * math.sqrt(k1 * k2 + k1 * k3 + k2 * k3)
    temp1 = k1 + k2 + k3
    # 2 curvatures
    nk0 = temp1 + temp0
    nk1 = temp1 - temp0
    # centers of tangent circles, 4 possibilities, but not all tangent.
    temp0 = 2.0 * cmath.sqrt(k1*k2*a[0]*b[0]+k1*k3*a[0]*c[0]+k2*k3*b[0]*c[0])
    temp1 = k1 * a[0] + k2 * b[0] + k3 * c[0]
    nc0 = (temp1 + temp0) / nk0
    nc1 = (temp1 - temp0) / nk1
    nc2 = (temp1 - temp0) / nk0
    nc3 = (temp1 + temp0) / nk1
    # radius of tangent circles
    r0 = 1.0 / nk0
    r1 = 1.0 / nk1
    # 4 possible circles given by
    c0 = nc0, r0
    c1 = nc1, r1
    c2 = nc2, r0
    c3 = nc3, r1
    # initialize a list
    lst = []
    # if c0 c1 are tangent to the 3 circles, return a list contain c0,c1
    if four_tangent(a, b, c, c0) and four_tangent(a, b, c, c1):
        lst.extend([c0, c1])
        return lst
    # if c2 c3 are tangent to the 3 circles, return a list contain c0,c1
    elif four_tangent(a, b, c, c2) and four_tangent(a, b, c, c3):
        lst.extend([c2, c3])
        return lst


# input a 3 mutually tangent circles and a list cs given in gasket().
# out put a new circle, might return None
def add_one_circle(a, b, c, cs):
    cirs = fourth_circle(a, b, c)
    # rule out the case fourth_circle returns None
    if cirs != None:
        # cir[0][1] is the radius, <0 means outer circles.
        # not in cs to avoid duplicate.
        if cirs[0] not in cs and cirs[0][1] > 0:
            return cirs[0]
        elif cirs[1] not in cs and cirs[1][1] > 0:
            return cirs[1]


# input a 3 mutually tangent circles and draw the 4th circle.
# also returns cs as used in gasket()
def draw_new_cir(a, b, c, cs):
    new_circle = add_one_circle(a, b, c, cs)
    if new_circle != None:
        # draw the circle
        cs.append(new_circle)
        dx = new_circle[0].real
        dy = new_circle[0].imag
        dr = abs(new_circle[1])
        draw.ellipse((pxy(dx - dr, dy - dr), pxy(dx + dr, dy + dr)))
        return cs


# this is the final function that takes 2 circles C1,C2 such that
# C1,C2,C0 are mutually tangent, and a number n, number of iteration.
def gasket(a,b,n):
    cs = [C0, a, b]
    # draw the 3 circles first
    for cir in cs:
        dx = cir[0].real
        dy = cir[0].imag
        dr = abs(cir[1])
        draw.ellipse((pxy(dx - dr, dy - dr), pxy(dx + dr, dy + dr)))
    # base case, also draw the 4th one, return the list of circles
    if n == 0:
        return cs
    if n == 1:
        cs = draw_new_cir(cs[0], cs[1], cs[2], cs)
        return cs
    else:
        # induction step
        cs = gasket(a, b, n-1)
        num = len(cs)
        # to iterate through every possible combination of 3 circles
        for i in range(0, num):
            for j in range(1, num):
                for k in range(2, num):
                    # make sure 3 different circles
                    if i!= j and i!= k and j!=k:
                        # make sure they are mutually tangent
                        if three_tangent(cs[i], cs[j], cs[k]):
                            # draw the new circle, also adds it to cs
                            draw_new_cir(cs[i], cs[j], cs[k], cs)
        # returns the list of circles for future use
        return cs


# input 2 circle a,b mutually tangent to C0, iteration number n.
# No output, but will show an image
def allopolian_gasket(a, b, n):
    global xmin, xmax, ymin, ymax, w, h, deltax, \
        deltay, draw, C0
    C0 = (complex(0.5, 0), -0.5)
    if not three_tangent(a, b, C0):
        print("input circles and C0 not mutually tangent")
    else:
        # initialize an image
        xmin=-0.5
        xmax=1.5
        ymin=-1
        ymax=1
        # numbers columns is 1000
        w = 1000
        h = 1000
        black = (0, 0, 0)
        bitmap = Image.new("RGB", (w, h), "white")
        pix = bitmap.load()   # this pixel matrix is called pix
        white=(255, 255, 255)
        deltax = abs(xmax - xmin)/w
        deltay = abs(ymax - ymin)/h
        draw = ImageDraw.Draw(bitmap)
        # to make the image all white
        for i in range(0, w):
            for j in range(0, h):
                pix[i, j] = (255, 255, 255)
        ######### Image initialized
        # to draw the disk D0 determined by C0.
        for i in range(0, w):
            for j in range(0, h):
                ## coord of the center of my i,j pixel
                x = xmin + (i + 1 / 2) * deltax
                y = ymin + (j + 1 / 2) * deltay
                temp = abs(complex(x,y)-1/2)
                if temp <= 1/2:
                    pix[i, h - j - 1] = black
        # end of initialize the image
        # call function gasket to draw
        gasket(a, b, n)
        bitmap.show()


# has a try
allopolian_gasket((complex(0.25, 0), 0.25), (complex(0.75, 0),
                                                 0.25), 5)


# to see different stages, delete both """
# 5 images will pop up, be careful =_=
# 5 images will pop up, be careful =_=
# 5 images will pop up, be careful =_=

"""
for i in range(1,6):
    allopolian_gasket((complex(0.25, 0), 0.25), (complex(0.75, 0),
                                               0.25), i)
                                               """


# to start from different inputs, delete both """
# 5 images will pop up, be careful =_=
# 5 images will pop up, be careful =_=
# 5 images will pop up, be careful =_=

"""
for i in range(1,6):
    allopolian_gasket((complex(0.5, 1/3), 1/6), (complex(0.75, 0),
                                                 0.25), i)
                                                 """
