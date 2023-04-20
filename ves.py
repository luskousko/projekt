from PIL import Image
from random import randint


def random_color():
  r = randint(0, 255)
  g = randint(0, 255)
  b = randint(0, 255)
  return (r, g, b)

def render_ves():
  width = 640
  height = 400
  img = Image.new('RGB', (width, height), (255,255,255))
  farba = random_color()
  for x in range(200, 401):
    for y in range(100, 201):
      img.putpixel((x, y), farba)
  return img

#1.LINEPIXELS-------------------------------------------------------------------------------
def linePixels(A, B):
  pixels = []
  if A[0] == B[0]:
    if A[1] > B[1]:
        A,B=B,A
    for y in range(A[1], B[1] + 1):
      pixels.append((A[0], y))
  elif A[1] == B[1]:
    if A[0] > B[0]:
        A,B=B,A
    for x in range(A[0], B[0] + 1):
      pixels.append((x, A[1]))
  else:
    if A[0] > B[0]:
        A,B=B,A
    dx = B[0] - A[0]
    dy = B[1] - A[1]
    if abs(dy/dx) > 1:
      for y in range(min(A[1], B[1]), max(A[1], B[1]) + 1):
        x = int((y - A[1] + (dy/dx) * A[0]) * (dx/dy))
        pixels.append((x, y))
    else:
      for x in range(min(A[0], B[0]), max(A[0], B[0]) + 1):
        y = int((B[1] - A[1])/(B[0] - A[0]) * (x - A[0]) + A[1])
        pixels.append((x, y))
  return pixels

#2.THICKLINE
def thick_line(im, A, B, thickness, color):
  pixels = linePixels(A, B)
  for X in pixels:
    FILL_CIRCLE(im, X, thickness/2, color)

#3.GET Y
def getY(point):
  return point[1]

#4.HEX TO RGB
def hex_to_rgb(hex):
  rgb = []
  for i in (0,2,4):                                          
    decimal = int(hex[i:i+2], 16)                
  return tuple(rgb)

#5.LINE
def line(im, A, B, color):
  if A[0] == B[0]:
    if A[1] > B[1]:
        A,B=B,A
    for y in range(A[1], B[1] + 1):
      im.putpixel((A[0], y), color)
  elif A[1] == B[1]:
    if A[0] > B[0]:
        A,B=B,A
    for x in range(A[0], B[0] + 1):
      im.putpixel((x, A[1]), color)
  else:
    if A[0] > B[0]:
        A,B=B,A
    dx = B[0] - A[0]
    dy = B[1] - A[1]
    if abs(dy/dx) > 1:
      for y in range(min(A[1], B[1]), max(A[1], B[1]) + 1):
        x = int((y - A[1] + (dy/dx) * A[0]) * (dx/dy))
        im.putpixel((x, y), color)
    else:
      for x in range(min(A[0], B[0]), max(A[0], B[0]) + 1):
        y = int((B[1] - A[1])/(B[0] - A[0]) * (x - A[0]) + A[1])
        im.putpixel((x, y), color)

#6.LINE2
def LINE(im, A, B, thickness, color):
  farba = hex_to_rgb(color)
  pixels = linePixels(A, B)
  for X in pixels:
    FILL_CIRCLE(im, X, thickness/2, farba)

#7.RECTANGLE
def RECT(im, ax, ay, width, height, thickness, color):
  farba = hex_to_rgb(color)
  LINE(obr, (ax,ay), (ax+width,ay), thickness, color) 
  LINE(obr, (ax+width,ay), (ax+width,ay+height), thickness, color)
  LINE(obr, (ax+width,ay+height), (ax,ay+height), thickness, color)
  LINE(obr, (ax,ay+height), (ax,ay), thickness, color)

#8.TRIANGLE
def TRIANGLE(im, ax, ay, bx, by, cx, cy, thickness, color):
  farba = hex_to_rgb(color)
  thick_line(obr, (ax, ay), (bx, by), thickness, farba)
  thick_line(obr, (ax, ay), (cx, cy), thickness, farba)
  thick_line(obr, (bx, by), (cx, cy), thickness, farba)

#9.CIRCLE
def CIRCLE(im, S, r, thickness, color):
  farba = hex_to_rgb(color)
  for x in range(0, int(r/2**(1/2)) + 1):
    y = int((r**2 - x**2)**(1/2))

    FILL_CIRCLE(obr , (x + S[0], y + S[1]), thickness/2, farba)
    FILL_CIRCLE(obr, (y + S[0], x + S[1]), thickness/2, farba)
    FILL_CIRCLE(obr, (y + S[0], -x + S[1]), thickness/2, farba)
    FILL_CIRCLE(obr, (x + S[0], -y + S[1]), thickness/2, farba)
    FILL_CIRCLE(obr, (-x + S[0], -y + S[1]), thickness/2, farba)
    FILL_CIRCLE(obr, (-y + S[0], -x + S[1]), thickness/2, farba)
    FILL_CIRCLE(obr, (-y + S[0], x + S[1]), thickness/2, farba)
    FILL_CIRCLE(obr, (-x + S[0], y + S[1]), thickness/2, farba)

#10.FILL CIRCLE
def FILL_CIRCLE(im, S, r, color):
  for x in range(0, int(r/2**(1/2)) + 1):
    y = int((r**2 - x**2)**(1/2))

    line(im, (x + S[0], y + S[1]), (x + S[0], -y + S[1]), color)
    line(im, (y + S[0], x + S[1]), (y + S[0], -x + S[1]), color)
    line(im, (-x + S[0], -y + S[1]), (-x + S[0], y + S[1]), color)
    line(im, (-y + S[0], -x + S[1]), (-y + S[0], x + S[1]), color)

#11.FILL TRIANGLE
def FILL_TRIANGLE(obr, ax, ay, bx, by, cx, cy, color):
  farba = hex_to_rgb(color) 
  A = (ax, ay)
  B = (bx, by)
  C = (cx, cy)
  V = sorted([A, B, C], key=getY)
  left = linePixels(V[0], V[1]) + linePixels(V[1], V[2])
  right = linePixels(V[0], V[2])
    
  Xmax = max(A[0], B[0], C[0])
  Xmin = min(A[0], B[0], C[0])
  if V[1][0] == Xmax:
    left, right = right, left

  for y in range(getY(V[0]), getY(V[2]) + 1):
    x1 = Xmax
    for X in left:
      if X[1] == y and X[0] < x1:
        x1 = X[0]
    
    x2 = Xmin
    for X in right:
      if X[1] == y and X[0] > x2:
        x2 = X[0]
    
    if x2 < 0:
      continue
    if x2 > obr.width:
      x2 = obr.width - 1
    if x1 < 0:
      x1 = 0

    line(obr, (x1, y), (x2, y), farba)

#12.FILL RECT
def FILL_RECT(im, ax, ay, width, height, fillcolor):
  fill_color = hex_to_rgb(fillcolor)
  for x in range(ax, ax+width+1):
    for y in range(ay, ay+height+1):
      obr.putpixel((x, y), fill_color)

#13. CLEAR
def CLEAR(color):
  farba = hex_to_rgb(color)
  for x in range(0, output_width):                             
    for y in range(0, output_height):
      obr.putpixel((x, y), farba)
  return obr
