# Playing with OpenCV

import cv2
import numpy as np
import math

heightThresh = 0 # not important right now

def process_img(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_red_min1 = 0
    hue_red_max1 = 20

    hue_red_min2 = 340
    hue_red_max2 = 360

    sat_red_min = 0.5
    sat_red_max = 1

    val_red_min = 0.4
    val_red_max = 1

    red_bounds1 = np.array([hue_red_min1/2, int(sat_red_min*255), int(val_red_min*255)]), np.array([hue_red_max2/2, int(sat_red_max*255), int(val_red_max*255)])
    red_bounds2 = np.array([hue_red_min2/2, int(sat_red_min*255), int(val_red_min*255)]), np.array([hue_red_max2/2, int(sat_red_max*255), int(val_red_max*255)])

    maskRed1 = cv2.inRange(hsv, red_bounds1[0], red_bounds1[1])
    maskRed2 = cv2.inRange(hsv, red_bounds2[0], red_bounds2[1])

    maskRed = cv2.bitwise_or(maskRed1,maskRed2)
    target = cv2.bitwise_and(img, img, mask=maskRed)

    cv2.imwrite("redMask.png", target)

    im, contours_red, hierarchy_red = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    redStr = "red"

    cv2.drawContours(img, contours_red, -1, (255,255,255), 3)

    #only looking for red contours
    if(len(contours_red) != 0):
        contArea = [(cv2.contourArea(c), (c)) for c in contours_red]
        contArea = sorted(contArea, reverse = True, key = lambda x:x[0])
        cont = contArea[0][1] # biggest one (I think)
        M = cv2.moments(cont)

        x,y,w,h = cv2.boundingRect(cont)
        print("red found")

        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            center = (cx,cy)
            cv2.circle(img, center, 5, (60,0,0), -1)

            cv2.rectangle(img, (x,y), (x+w, y+h), (100,50,50),2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, redStr, center, font, 1, (0,0,0), 4)

    else:
        print("No red shapes found")



    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    return img

file_name = 'geometric_shapes.jpg'

# load image
img = cv2.imread(file_name, 1)

# draw contour
processed = process_img(img)

# display both images
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

cv2.imshow('processed image', processed)
cv2.waitKey(0)
cv2.destroyAllWindows()
