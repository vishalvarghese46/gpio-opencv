import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(r'E:\Python\OpenCVLearning\OpenCV\images\vedhika.jpg', 0)

cv2.imshow('image', img)
cv2.waitKey(0) #waits for any key to be pressed
cv2.destroyAllWindows()