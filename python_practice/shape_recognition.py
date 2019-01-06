import numpy as np
import cv2
import math
#import imutils
from masks import *

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self,c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04*peri, True)
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)

        if len(approx) == 3:
            # any shape with 3 vertices is a triangle
            shape = "triangle"
        elif len(approx) == 4:
            # shape is either a shapre or a rectangle
            # compute bounding rectangle of contour and use it to compute
            # the aspect ratio
            (x,y,w,h) = cv2.boundingRect(approx)
            ar = w/float(h)

            if ((ar >= 0.95) and (ar <= 1.05)):
                shape = "square"
            else:
                shape = "rectangle"
        elif len(approx) == 5:
            shape = "pentagon"
        elif len(approx) == 6:
            shape = "hexagon"
        elif len(approx) == 7:
            shape = "heptagon"
        elif len(approx) == 8:
            shape = "octagon"
        elif (0.22 <= ((4*pi*area)/ (perimeter^2)) and 0.28 >= ((4*pi*area)/ (perimeter^2))):
            shape = "star"
        else:
            shape = "circle"

        return shape

sd = ShapeDetector()


def label_contour_shapes(contours, img, color):
    for c in contours:
        # add a check for the size of the contour
        #print("blue found")
        M = cv2.moments(c)
        shape = sd.detect(c)

        x,y,w,h = cv2.boundingRect(c)

        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            center = (cx,cy)
            cv2.circle(img, center, 5, (60,0,0), -1)

            #cv2.rectangle(img, (x,y), (x+w, y+h), (100,50,50),2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, shape, center, font, 1, (0,0,0), 2)

def process_img(img):

    maskBlue = mask(img, "blue")
    maskRed = mask(img, "red")
    maskYellow = mask(img, "yellow")
    maskGreen = mask(img, "green")

    im, contours_blue, hierarchy_blue = cv2.findContours(maskBlue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im, contours_red, hierarchy_red = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im, contours_yellow, hierarchy_yellow = cv2.findContours(maskYellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im, contours_green, hierarchy_green = cv2.findContours(maskGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours_blue, -1, (0,0,0), 3)
    cv2.drawContours(img, contours_red, -1, (0,255,255), 3)
    cv2.drawContours(img, contours_yellow, -1, (255,0,255), 3)
    cv2.drawContours(img, contours_green, -1, (255,255,0), 3)

    label_contour_shapes(contours_blue, img, "Blue")
    label_contour_shapes(contours_red, img, "Red")
    label_contour_shapes(contours_yellow, img, "Yellow")
    label_contour_shapes(contours_green, img, "Green")

    #cv2.imshow('with_contours', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return img


file_name = 'source_images/geometric_shapes.jpg'
# load image
img = cv2.imread(file_name, 1)

processed = process_img(img) # actually edits original

cv2.imwrite('results/shape_recognition.png', processed)

cv2.imshow('processed image', processed)
cv2.waitKey(0)
cv2.destroyAllWindows()
