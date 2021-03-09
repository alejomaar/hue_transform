import cv2
import numpy as np

img = cv2.imread('Renderfinal.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv[:,:,0]=(hsv[:,:,0]+50)%180
bgrimg = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

cv2.imshow('Example - Show image in window',bgrimg )
cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image