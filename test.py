import cv2 as cv
import numpy as np 

x = 2
v = 2*np.pi + x

print( v)

# Create a blank black rectangle (e.g., 400x300 pixels)
height, width = 300, 400
blank = np.zeros((height, width, 3), dtype=np.uint8)
# Optionally display the image (uncomment if you want to see it)
cv.imshow('Blank Rectangle', blank)
cv.waitKey(0)
cv.destroyAllWindows()

