# Playing with OpenCV

import cv2
import numpy as np
import math

heightThresh = 0 # not important right now

def process_img(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_green_min = 80
    hue_green_max = 160

    sat_green_min = 0.5
    sat_green_max = 1

    val_green_min = 0.4
    val_green_max = 1

    green_bounds = np.array([hue_green_min/2, int(sat_green_min*255), int(val_green_min*255)]), np.array([hue_green_max/2, int(sat_green_max*255), int(val_green_max*255)])

    maskGreen = cv2.inRange(hsv, green_bounds[0], green_bounds[1])
    im, contours_green, hierarchy_green = cv2.findContours(maskGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    greenStr = "green"

    try:
        for i in range(len(contours_green)):
            if len(contours_green[i]) != 0:
                contArea = [(cv2.contourArea(c), (c)) for c in contours_green[i]]
                contArea = sorted(contArea, reverse = True, key = lambda x: x[0])

                cont = contArea[0][1]

                M = cv2.moments(cont)

                x,y,w,h = cv2.boundingRect(cont)
                contour_height = h

                if contour_height > heightThresh:
                    print(greenStr, "found")
                    cv2.drawContours(img, cont, -1, (255,255,255), 10)

                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])

                        center = (cx, cy)
                        cv2.circle(img, center, 5, (60,0,0), -1)

                        cv2.rectangle(img, (x,y), (x + w, y + h), (100, 50, 50), 2)

                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(img, greenStr, center, font, 1, (0,0,0), 4)


    except Exception as e:
        print(str(e))

    return img

file_name = 'four_colors.png'

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
