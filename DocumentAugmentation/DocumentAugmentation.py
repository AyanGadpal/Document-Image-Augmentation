from random import randint
import cv2
import numpy as np

# Apply basic Thresholding
def basicTransform(img):
	_, mask = cv2.threshold(img,220,255,cv2.THRESH_BINARY_INV)
	img = cv2.bitwise_not(mask)
	return img

# Change The background color (currently assumed white) to random color
def changeColor(image):
  # Color list to select color from
  colorList = [[228,238,240],[148,236,255],[174,174,255],[103,255,220],[124,229,176],[231,216,180]]
  # Random index
  randomColor = randint(0,5)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ret, mask = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
  # Making a copy
  coloredImage = image.copy()
  # Changing color
  coloredImage[mask == 0] = colorList[randomColor]
  return coloredImage

# Increase the Brightness
def BrightnessUp(image,alpha=50.0):
  alpha = float(alpha)
  image = cv2.add(image,np.array([alpha]))
  return image

# Decrease the Brightness
def BrightnessDown(image,alpha=50.0):
  alpha = float(alpha)
  image = cv2.subtract(image,np.array([alpha]))
  return image

# Smudging
def Smudge(image):
  b,g,r = cv2.split(image)
  
  # Apply Basic Transformation
  b = basicTransform(b)
  r = basicTransform(r)
  g = basicTransform(g)
  
  # Perform the distance transform algorithm
  b = cv2.distanceTransform(b, cv2.DIST_L2, 5)  # ELCUDIAN
  g = cv2.distanceTransform(g, cv2.DIST_L1, 5)  # LINEAR
  r = cv2.distanceTransform(r, cv2.DIST_C, 5)   # MAX

  # Normalize
  r = cv2.normalize(r, r, 0, 1.0, cv2.NORM_MINMAX)
  g = cv2.normalize(g, g, 0, 1.0, cv2.NORM_MINMAX)
  b = cv2.normalize(b, b, 0, 1.0, cv2.NORM_MINMAX)

  # Merge the channels
  dist = cv2.merge((b,g,r))
  dist = cv2.normalize(dist,dist, 0, 4.0, cv2.NORM_MINMAX)
  dist = cv2.cvtColor(dist, cv2.COLOR_BGR2GRAY)

  # In order to save as jpg, or png, we need to handle the Data
  # format of image
  data = dist.astype(np.float64) / 4.0
  data = 1800 * data # Now scale by 1800
  SmudgedImage = data.astype(np.uint16)

  return SmudgedImage

# Dialate
def Dialate(image,kernal=np.ones((2,2),np.uint8)):
  _, mask = cv2.threshold(image,220,255,cv2.THRESH_BINARY_INV)
  dst = cv2.dilate(mask,kernal,iterations = 1)
  DialatedImage = cv2.bitwise_not(dst)
  return DialatedImage
