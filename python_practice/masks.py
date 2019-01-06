# practice with creating masks with different colors
import cv2
import numpy as np
import math

def mask(img, color):
    # takes an OpenCV image and a string color ("blue", "yellow", "green", "red")
    # returns a mask for the given color
    if (color == "red"):
        mask = redMask(img)
    elif (color == "yellow"):
        mask = yellowMask(img)
    elif (color == "blue"):
        mask = blueMask(img)
    elif (color == "green"):
        mask = greenMask(img)
    else:
        print("Error, invalid color option")

    return mask


def blueMask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_blue_min = 100
    hue_blue_max = 130

    sat_blue_min = 0.5
    sat_blue_max = 1

    val_blue_min = 0.4
    val_blue_max = 1

    blue_bounds = np.array([hue_blue_min, int(sat_blue_min*255), int(val_blue_min*255)]), np.array([hue_blue_max, int(sat_blue_max*255), int(val_blue_max*255)])

    maskBlue = cv2.inRange(hsv, blue_bounds[0], blue_bounds[1])

    return maskBlue;

def yellowMask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_yellow_min = 20
    hue_yellow_max = 35

    sat_yellow_min = 0.5
    sat_yellow_max = 1

    val_yellow_min = 0.4
    val_yellow_max = 1

    yellow_bounds = np.array([hue_yellow_min, int(sat_yellow_min*255), int(val_yellow_min*255)]), np.array([hue_yellow_max, int(sat_yellow_max*255), int(val_yellow_max*255)])

    maskYellow = cv2.inRange(hsv, yellow_bounds[0], yellow_bounds[1])

    return maskYellow;

def greenMask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_green_min = 40
    hue_green_max = 75

    sat_green_min = 0.5
    sat_green_max = 1

    val_green_min = 0.4
    val_green_max = 1

    green_bounds = np.array([hue_green_min, int(sat_green_min*255), int(val_green_min*255)]), np.array([hue_green_max, int(sat_green_max*255), int(val_green_max*255)])

    maskGreen = cv2.inRange(hsv, green_bounds[0], green_bounds[1])

    return maskGreen;

def redMask(img):
    # gets red and dark orange
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #hue_red_min = 0
    #hue_red_max = 20

    #sat_red_min = 0.5
    #sat_red_max = 1

    #val_red_min = 0.4
    #val_red_max = 1

    red_bounds_1 = np.array([0, int(0.5*255), int(0.4*255)]), np.array([20, int(1*255), int(1*255)])
    red_bounds_2 = np.array([165, int(0.5*255), int(0.4*255)]), np.array([180, int(1*255), int(1*255)])

    maskRed1 = cv2.inRange(hsv, red_bounds_1[0], red_bounds_1[1])
    maskRed2 = cv2.inRange(hsv, red_bounds_2[0], red_bounds_2[1])

    maskRed = cv2.bitwise_or(maskRed1, maskRed2)

    return maskRed;

# ADD MORE AS NEEDED! :)


#file_name = 'source_images/geometric_shapes.jpg'
# load image

#original = cv2.imread(file_name, 1)
#blue = blueMask(original)
#red = redMask(original)
#yellow = yellowMask(original)
#green = greenMask(original)

#cv2.imshow('original image', original)
#cv2.imshow('blue mask', blue)
#cv2.imshow('red mask', red)
#cv2.imshow('yellow mask', yellow)
#cv2.imshow('green mask', green)

#cv2.imwrite('masks/blueMask.png', blue)
#cv2.imwrite('masks/redMask.png', red)
#cv2.imwrite('masks/yellowMask.png', yellow)
#cv2.imwrite('masks/greenMask.png', green)

#cv2.waitKey(0)
#cv2.destroyAllWindows()
