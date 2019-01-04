# Playing with OpenCV
import cv2
import numpy as np
import math
from mask_prac import *

heightThresh = 0 # not important right now

def label_contours(contours, img, color):
    for c in contours:
        #print("blue found")
        M = cv2.moments(c)

        x,y,w,h = cv2.boundingRect(c)

        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            center = (cx,cy)
            cv2.circle(img, center, 5, (60,0,0), -1)

            cv2.rectangle(img, (x,y), (x+w, y+h), (100,50,50),2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, color, center, font, 1, (0,0,0), 4)

def process_img(img):

    maskBlue = blueMask(img)
    maskRed = redMask(img)
    maskYellow = yellowMask(img)
    maskGreen = greenMask(img)

    im, contours_blue, hierarchy_blue = cv2.findContours(maskBlue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im, contours_red, hierarchy_red = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im, contours_yellow, hierarchy_yellow = cv2.findContours(maskYellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im, contours_green, hierarchy_green = cv2.findContours(maskGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours_blue, -1, (0,0,0), 3)
    cv2.drawContours(img, contours_red, -1, (0,255,255), 3)
    cv2.drawContours(img, contours_yellow, -1, (255,0,255), 3)
    cv2.drawContours(img, contours_green, -1, (255,255,0), 3)

    label_contours(contours_blue, img, "Blue")
    label_contours(contours_red, img, "Red")
    label_contours(contours_yellow, img, "Yellow")
    label_contours(contours_green, img, "Green")

    #cv2.imshow('with_contours', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return img

file_name = 'source_images/geometric_shapes.jpg'

# load image
img = cv2.imread(file_name, 1)

# draw contour
processed = process_img(img) # actually edits original

# display both images
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

cv2.imwrite('results/color_recognition.png', processed)

cv2.imshow('processed image', processed)
cv2.waitKey(0)
cv2.destroyAllWindows()
