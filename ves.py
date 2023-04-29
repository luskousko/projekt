from PIL import Image
from random import randint

def hex2dec(cislo):
  vysledok = 0
  for index in range(len(cislo)):
    cifra = cislo[(index+1)*(-1)].upper()   
    if ord("A") <= ord(cifra) <= ord("F"):
      cifra = ord(cifra) - 65 + 10
    else:
      cifra = int(cifra)
    vysledok += cifra*16**index
  return vysledok

def hexColor(color):
  r = hex2dec(color[1:3])
  g = hex2dec(color[3:5])
  b = hex2dec(color[5:7])
  return (r, g, b)

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

def fill_circle(im, S, r, color):
  for x in range(0, int(r/2**(1/2)) + 1):
    y = int((r**2 - x**2)**(1/2))
    line(im, (x + S[0], y + S[1]), (x + S[0], -y + S[1]), color)
    line(im, (y + S[0], x + S[1]), (y + S[0], -x + S[1]), color)
    line(im, (-x + S[0], -y + S[1]), (-x + S[0], y + S[1]), color)
    line(im, (-y + S[0], x + S[1]), (-y + S[0], -x + S[1]), color)

def fill_rect(im, A, width, height, color):
  for x in range(A[0], A[0] + width):
    for y in range(A[1], A[1] + height):
      im.putpixel((x, y), color)


def thick_line(im, A, B, thickness, color):
  pixels = linePixels(A, B)
  for X in pixels:
    fill_circle(im, X, thickness/2, color)


def rect(im, A, width, height, thickness, color):
  #thick_line(im, A, (A[0]+ width, A[1] + height), thickness, color)
  thick_line(im, A, (A[0]+ width, A[1]), thickness, color)
  thick_line(im, (A[0]+ width, A[1]), (A[0]+ width, A[1] + height), thickness, color)
  thick_line(im, A, (A[0], A[1] + height), thickness, color)
  thick_line(im, (A[0], A[1] + height), (A[0] + width, A[1] + height), thickness, color)

def triangle(im, A, B, C, thickness, color):
  thick_line(im, A, B, thickness, color)
  thick_line(im, A, C, thickness, color)
  thick_line(im, C, B, thickness, color)

def getY(point):
  return point[1]

def fill_triangle(im, A, B, C, color):
  #Nakrelis do obrazku im trojuhlnik s bodmi ABC a farbou color
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
    if x2 > im.width:
      x2 = im.width - 1
    if x1 < 0:
      x1 = 0
    line(im, (x1, y), (x2, y), color)



def circle(im, S, r, thickness, color):
  for i in range(thickness):
    for x in range(0, int(r/2**(1/2)) + 1 ):
      y = int((r**2 - x**2)**(1/2))
      im.putpixel((x + S[0], y + S[1]), color)
      im.putpixel((y + S[0], x + S[1]), color)
      im.putpixel((y + S[0], -x + S[1]), color)
      im.putpixel((x + S[0], -y + S[1]), color)
      im.putpixel((-x + S[0], -y + S[1]), color)
      im.putpixel((-y + S[0], -x + S[1]), color)
      im.putpixel((-y + S[0], x + S[1]), color)
      im.putpixel((-x + S[0], y + S[1]), color)
    r = r - 1

def random_color():
  r = randint(0, 255)
  g = randint(0, 255)
  b = randint(0, 255)
  return (r, g, b)

clear_color = (255, 255, 255)

def render_ves(ves):
    try:
      first_line = ves[0]
      first_line = first_line.split(" ")
      width = int(first_line[2])
      height = int(first_line[3])

      img = Image.new('RGB', (int(width), int(height)), (255, 255, 255))
      #print(ves)
    
      for line in ves:
          line = line.split(" ")
          #print(line)
          if line[0] == "CIRCLE":
              circle_color = hexColor(line[5])
              circle(img, (round(float(line[1])), round(float(line[2]))), round(float(line[3])), round(float(line[4])), circle_color)

          elif line[0] == "CLEAR":
              clear_color = hexColor(line[1])
              fill_rect(img, (0, 0), width, height, clear_color)

          elif line[0] == "FILL_CIRCLE":
              fcircle_color = hexColor(line[4])
              fill_circle(img, (round(float(line[1])), round(float(line[2]))), round(float(line[3])), fcircle_color)

          elif line[0] == "LINE":
              line_color = hexColor(line[6])
              thick_line(img, (round(float(line[1])), round(float(line[2]))), (round(float(line[3])), round(float(line[4]))), round(float(line[5])), line_color)                

          elif line[0] == "FILL_RECT":
              frect_color = hexColor(line[5])
              fill_rect(img, (round(float(line[1])), round(float(line[2]))), round(float(line[3])), round(float(line[4])), frect_color)
          
          elif line[0] == "RECT":
              rect_color = hexColor(line[6])
              rect(img, (round(float(line[1])), round(float(line[2]))), round(float(line[3])), round(float(line[4])), round(float(line[5])), rect_color)

          elif line[0] == "TRIANGLE":
              triangle_color = hexColor(line[8])
              triangle(img, (round(float(line[1])), round(float(line[2]))), (round(float(line[3])), round(float(line[4]))), (round(float(line[5])), round(float(line[6]))),round(float(line[7])) ,triangle_color)

          elif line[0] == "FILL_TRIANGLE":
              ftriangle_color = hexColor(line[7])
              fill_triangle(img, (round(float(line[1])), round(float(line[2]))), (round(float(line[3])), round(float(line[4]))), (round(float(line[5])), round(float(line[6]))), ftriangle_color)
   except:
      img = Image.new('RGB', (500, 500), (255, 255, 255))
      fill_triangle(img, (250, 250), (200, 100), (300, 100),(255,0,0))
      fill_circle(img, (250, 300), 30, (255, 0, 0))
      return img
    return img
