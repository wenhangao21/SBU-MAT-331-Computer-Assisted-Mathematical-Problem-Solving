from PIL import Image, ImageColor, ImageDraw
from cmath import *
from math import *
# Note: output images will be saved to the same directory where you
# store this .py file.
# images will not pop up, will just be saved.
# initialize an image
xmin = -5/2
xmax = 5/2
ymin = -5/2
ymax = 5/2
w = 500
h = 500
bitmap = Image.new("RGB", (w, h), "white")
pix = bitmap.load()
deltax = abs(xmax - xmin)/w
deltay = abs(ymax - ymin)/h


# input z and c, out put the greens function value
def green_function(zx0, zy0, c):
    if zx0 == 0 and zy0 == 0:
        return 0
    z = complex(zx0, zy0)
    logf = log(abs(z))
    fac = 1/2
    n = 0
    # if <= 0, always in the julia set
    if logf <= 0:
        return 0
    else:
        # implement the algorithm found in 2
        while n < 50 and abs(z)<1e24:
            z = z*z+c
            logf = logf +fac*log(abs(1+c/(z*z)))
            n = n+1
            fac = fac*fac
        return logf


# input z and c, output a 3 tuple of RGB value
def u(zx0, zy0, c):
    x = green_function(zx0, zy0, c)
    if x <= 0:
        return 0, 0, 0
    else:
        r = (128+floor(10000*x/128)) % 256
        g = floor(log2(log2(x))) % 256
        b = floor(100*log2(x)) % 256
        return r, g, b


# input z and c, output a 3 tuple of RGB value
def v(zx0, zy0, c):
    x = green_function(zx0, zy0, c)
    if x <= 1:
        return 0, 0, 0
    else:
        r = floor(255*(1+cos(2*sqrt(2)*pi*log(x)))/2)
        g = floor(255*(1+cos(2*sqrt(3)*pi*log(x)))/2)
        b = floor(255*(1+cos(2*sqrt(3)*pi*log(log(x))))/2)
        return r, g, b


# input the pix matrix and c. no output, just coloring by u
def julia_u(pix, c):
    global xmin, xmax, ymin, ymax, deltax, deltay, w, h
    cx = c.real
    cy = c.imag
    for i in range(0, w):
        for j in range(0, h):
            x = xmin + i * deltax
            y = ymin + j * deltay
            # init z0
            zx = x
            zy = y
            maxiter = 100
            snorm = x * x + y * y
            iterations = 0
            while (snorm <= 1000) and (iterations <= maxiter):
                a = zx * zx - zy * zy + cx
                b = 2 * zx * zy + cy
                zx = a
                zy = b
                snorm = zx * zx + zy * zy
                iterations += 1
            snorm = zx * zx + zy * zy
            if (snorm >= 1000):
                # not in the julia set, needs coloring
                pix[i, h - j - 1] = u(zx, zy, c)
            else:
                # in the julia set, just set it as black
                pix[i, h - j - 1] = (0, 0, 0)


# input the pix matrix and c. no output, just coloring by v
def julia_v(pix, c):
    global xmin, xmax, ymin, ymax, deltax, deltay, w, h, white, black
    cx = c.real
    cy = c.imag
    for i in range(0, w):
        for j in range(0, h):
            x = xmin + i * deltax
            y = ymin + j * deltay
            # init z0
            zx = x
            zy = y
            maxiter = 100
            snorm = x * x + y * y
            iterations = 0
            while (snorm <= 1000) and (iterations <= maxiter):
                a = zx * zx - zy * zy + cx
                b = 2 * zx * zy + cy
                zx = a
                zy = b
                snorm = zx * zx + zy * zy
                iterations += 1
            snorm = zx * zx + zy * zy
            if (snorm >= 1000):
                # not in the julia set
                pix[i, h - j - 1] = v(zx, zy, c)
            else:
                # in the julia set
                pix[i, h - j - 1] = (0, 0, 0)


# input the pix matrix no output, just coloring by u
def mandelbrot_u(pix):
    global xmin,xmax, ymin,ymax, deltax,deltay,w,h

    for i in range(0,w):
        for j in range (0,h):
            cx=xmin+ i *deltax
            cy=ymin+j*deltay
            c = complex(cx, cy)
            zx=0
            zy=0
            maxiter=100
            snorm= zx*zx+zy*zy
            iterations=0
            while ((snorm<=1000) and (iterations<= maxiter)):
                a= zx*zx - zy*zy + cx
                b= 2*zx* zy + cy
                zx=a
                zy=b
                snorm= zx*zx + zy*zy
                iterations+=1
            snorm= zx*zx + zy*zy
            if (snorm >=1000):
                ### not in mandelbrot s
                pix[i,h-j-1] = u(zx, zy, c)
            else:
                pix[i,h-j-1]=(0, 0, 0)


# input the pix matrix no output, just coloring by v
def mandelbrot_v(pix):
    global xmin,xmax, ymin,ymax, deltax,deltay,w,h

    for i in range(0,w):
        for j in range (0,h):
            cx=xmin+ i *deltax
            cy=ymin+j*deltay
            c = complex(cx, cy)
            zx=0
            zy=0
            maxiter=100
            snorm= zx*zx+zy*zy
            iterations=0
            while ((snorm<=1000) and (iterations<= maxiter)):
                a= zx*zx - zy*zy + cx
                b= 2*zx* zy + cy
                zx=a
                zy=b
                snorm= zx*zx + zy*zy
                iterations+=1
            snorm= zx*zx + zy*zy
            if (snorm >=1000):
                ### not in mandelbrot s
                pix[i,h-j-1] = v(zx, zy, c)
            else:
                pix[i,h-j-1]=(0, 0, 0)


c0 = complex(0, 0)
c1 = complex(-0.123, 0.745)
c2 = complex(-1, 0)
c3 = complex(0.3, 0.5)
c4 = complex(-0.8, 0.156)
C = c0, c1, c2, c3, c4
# Exercice 1 (3)

for c in C:
    i = 0
    julia_u(pix, c)
    bitmap.save("julia_u"+str(c)+".jpg")



# Exercise 1 (4)

for c in C:
    julia_v(pix, c)
    bitmap.save("julia_v"+str(c)+".jpg")



# Exercise 2 (3)

mandelbrot_u(pix)
bitmap.save("mandelbrot_u.jpg")



# Exercise 2 (4)

mandelbrot_v(pix)
bitmap.save("mandelbrot_v.jpg")



# Exercise 2 (5)

xmin1 = -0.25
xmax1 = 0.75
ymin1 = -0.5
ymax1 = 0.5
# umbers columns is 500
w1 = 500
h1 = 500
bitmap1 = Image.new("RGB", (w1, h1), "white")
pix1 = bitmap1.load()
deltax1 = abs(xmax1 - xmin1)/w1
deltay1 = abs(ymax1 - ymin1)/h1


# not going to be used, just another coloring function
def bdy(zx0, zy0, c):
    x = green_function(zx0, zy0, c)
    if x <= 0:
        return 0, 0, 0
    else:
        r = floor(255*(1+cos(2*pi*x))/2)
        g = floor(255*(1+cos(2*pi*x))/2)
        b = floor(255*(1+cos(2*pi*x))/2)
        return r, g, b

# coloring function
def bdy1(zx0, zy0, c):
    x = green_function(zx0, zy0, c)
    if x <= 0:
        return 0, 0, 0
    else:
        b = 7
        r = floor(255*(1+cos(2*sqrt(7)*pi*log(x)))/2)
        g = floor(255*(1-cos(b*x))/2)
        b = floor(255*(1+cos(2*sqrt(5)*pi*log(log(x))))/2)
        return r, g, b


# input the pix matrix no output, just coloring by bdy1
def mandelbrot_bdy1(pix):
    global xmin1,xmax1, ymin1,ymax1, deltax1,deltay1,w1,h1

    for i in range(0,w1):
        for j in range (0,h1):
            cx=xmin1 + i * deltax1
            cy=ymin1 + j * deltay1
            c = complex(cx, cy)
            zx=0
            zy=0
            maxiter=100
            snorm= zx*zx+zy*zy
            iterations=0
            while ((snorm<=1000) and (iterations<= maxiter)):
                a= zx*zx - zy*zy + cx
                b= 2*zx* zy + cy
                zx=a
                zy=b
                snorm= zx*zx + zy*zy
                iterations+=1
            snorm= zx*zx + zy*zy
            if (snorm >=1000):
                # not in mandelbrot s, needs coloring
                pix[i,h-j-1] = bdy1(zx, zy, c)
            else:
                pix[i,h-j-1]=(0, 0, 0)


mandelbrot_bdy1(pix1)
bitmap1.save("mandelbrot_bdy1.jpg")

