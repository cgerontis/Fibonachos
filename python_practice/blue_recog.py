# Playing with OpenCV

import cv2
import numpy as np
import math
#from mask_prac import *

def process_img(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_blue_min = 100
    hue_blue_max = 130

    sat_blue_min = 0.5
    sat_blue_max = 1

    val_blue_min = 0.4
    val_blue_max = 1

    blue_bounds = np.array([hue_blue_min, int(sat_blue_min*255), int(val_blue_min*255)]), np.array([hue_blue_max, int(sat_blue_max*255), int(val_blue_max*255)])

    maskblue = cv2.inRange(hsv, blue_bounds[0], blue_bounds[1])

    #maskblue = cv2.bitwise_or(maskblue1,maskblue2)
    #target = cv2.bitwise_and(img, img, mask=maskblue)

    #cv2.imwrite("blueMask.png", target)

    im, contours_blue, hierarchy_blue = cv2.findContours(maskblue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    blueStr = "blue"

    cv2.drawContours(img, contours_blue, -1, (255,255,255), 3)

    #only looking for blue contours
    if(len(contours_blue) != 0):
        contArea = [(cv2.contourArea(c), (c)) for c in contours_blue]
        contArea = sorted(contArea, reverse = True, key = lambda x:x[0])
        cont = contArea[0][1] # biggest one (I think)
        M = cv2.moments(cont)

        x,y,w,h = cv2.boundingRect(cont)
        print("blue found")

        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            center = (cx,cy)
            cv2.circle(img, center, 5, (60,0,0), -1)

            cv2.rectangle(img, (x,y), (x+w, y+h), (100,50,50),2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, blueStr, center, font, 1, (0,0,0), 4)

    else:
        print("No blue shapes found")



    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    return img

file_name = 'geometric_shapes.jpg'

# load image
img = cv2.imread(file_name, 1)

# draw contour(s)
processed = process_img(img)

# display both images
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

cv2.imshow('processed image', processed)
cv2.waitKey(0)
cv2.destroyAllWindows()
