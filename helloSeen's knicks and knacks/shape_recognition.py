# import the necessary packages
import imutils
import cv2
import random
import math
import numpy
import os
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
#The following following loop picks a random image in the training set
#Since the image numbering sometimes skips a number, we use the loop to
#check if it exists
string = ''
while (not os.path.isfile('C:/Users/Sean Nemtzow/Downloads/Data_Training/Data_Training/' + string)):
        file_num = random.randint(5,10000)
        log = math.ceil(math.log10(file_num))
        string = 'IMG_'
        for x in range(4-log):
                string += '0'
        string += str(file_num)
        string += '.jpg'
print(string)

#Load the image
image = cv2.imread('C:/Users/Sean Nemtzow/Downloads/Data_Training/Data_Training/' + string)
 
# convert the resized image to grayscale, blur it slightly,
# and create 2 thresholds at different intensities
resized = imutils.resize(image, width=900)
ratio = image.shape[0] / float(resized.shape[0])
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
thresh_low = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
thresh_high = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

 
# find contours in the thresholded images 
cnts_low = cv2.findContours(thresh_low.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
cnts_low = imutils.grab_contours(cnts_low)
cnts_high = cv2.findContours(thresh_high.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
cnts_high = imutils.grab_contours(cnts_high)

#This is a saved contour of the upper_left_corner of the gate,
#we will use this to compare the contours we find to this
upper_left = numpy.load('upper_left_contour.npy')
#Next we will iterate through the contours we found in each threshold and filter through them
# loop over the contours in the low threshold
for c in cnts_low:
        #If the contour is small, ignore it (helps reduce garbage)
        M = cv2.moments(c)
        if (M["m00"] < 10):
                continue
        #Compare the contour to the saved upper_left_corner contour, if it's close in shape keep it
        #Otherwise ignore it
        if(cv2.matchShapes(c,upper_left,1,0.0) > 1):
                continue
        #Create a rectangle around the contours we like and label them
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image,(int(x*ratio),int(y*ratio)),(int((x+w)*ratio),int((y+h)*ratio)), (0,0,255),2)
        cv2.putText(image, 'Corner', (int(x*ratio),int(y*ratio)), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2, cv2.LINE_AA)
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

#Loop through contours in high threshold
for c in cnts_high:
        #If the contour is small, ignore it (helps reduce garbage)
        M = cv2.moments(c)
        if (M["m00"] < 10):
                continue
        #Compare the contour to the saved upper_left_corner contour, if it's close in shape keep it
        #Otherwise ignore it
        if(cv2.matchShapes(c,upper_left,1,0.0) > 1):
                continue
        #Create a rectangle around the contours we like and label them
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image,(int(x*ratio),int(y*ratio)),(int((x+w)*ratio),int((y+h)*ratio)), (0,0,255),2)
        cv2.putText(image, 'Corner', (int(x*ratio),int(y*ratio)), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2, cv2.LINE_AA)
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

#Show the final image
cv2.imshow("Image", image)
#cv2.imwrite('randomTest_' + string,image) #Uncomment this if you want to save the results
