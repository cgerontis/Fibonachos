# import the necessary packages
import imutils
import cv2
import random
import math
import numpy
import os
from operator import itemgetter
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
#The following following loop picks a random image in the training set
#Since the image numbering sometimes skips a number, we use the loop to
#check if it exists
string = ''
while (not os.path.isfile('ADDRESS TO DATA TRAINING FOLDER' + string)):
        file_num = random.randint(5,10000)
        log = math.ceil(math.log10(file_num))
        string = 'IMG_'
        for x in range(4-log):
                string += '0'
        string += str(file_num)
        string += '.jpg'
print(string)

#Load the image
image = cv2.imread('ADDRESS TO DATA TRAINING FOLDER' + string)
 
# convert the resized image to grayscale, blur it slightly,
# use a Canny threshold and then blur it again
resized = imutils.resize(image, width = 800)
ratio = image.shape[0] / float(resized.shape[0])
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (13, 13), 0)
detected = cv2.Canny(blurred, 80, 120, 3)
blur_again = blurred = cv2.GaussianBlur(detected, (3, 3), 0)

# find contours in the thresholded image
cnts_low = cv2.findContours(blur_again.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
cnts_low = imutils.grab_contours(cnts_low)

#This is a saved contour of the upper_left_corner of the gate,
#we will use this to compare the contours we find to this
upper_left = numpy.load('upper_left_contour.npy')
#Next we will iterate through the contours we found in the threshold and filter through them

# loop over the contours
filtered_by_area = []
for c in cnts_low:
        #If the contour is small, ignore it (helps reduce garbage)
        M = cv2.moments(c)
        if (M["m00"] < 10):
                continue
        #Compare the contour to the saved upper_left_corner contour, if it's close in shape keep it
        #Otherwise ignore it
        if(cv2.matchShapes(c,upper_left,1,0.0) > 1.5):
                continue
        filtered_by_area.append([M["m00"],c,M["m10"],M["m01"]])

#Grab the 4 biggest contours

filtered_by_area = sorted(filtered_by_area, key = itemgetter(0))

filtered_by_area = filtered_by_area[-4:]

#If we grabbed at least 3 contours, use them to determine the gate
#If we didn't, use the hough line analysis
coord_track = []
if (len(filtered_by_area) > 2):
        for pair in filtered_by_area:
                c = pair[1]
                x,y,w,h = cv2.boundingRect(c)
                Cx = int(round(pair[2]/pair[0]*ratio))
                Cy = int(round(pair[3]/pair[0]*ratio))
                topX = int(round(x*ratio))
                topY = int(round(y*ratio))
                bottomX = int(round((x+w)*ratio))
                bottomY = int(round((y+h)*ratio))
                #Determines the orientation of the corner by finding the closest corner
                #To the calculated centroid of the shape
                if (abs(topX-Cx) > abs(bottomX-Cx)):
                        x_point = topX + w*0.85
                else:
                        x_point = bottomX - w*0.85
                if (abs(topY-Cy) > abs(bottomY-Cy)):
                        y_point = topY + h*0.75
                else:
                        y_point = bottomY - h*0.75
                #The checkered corners hold a pretty consistent relationship with their position
                #And where the inside of the gate is, above we calculated the coordinates of the
                #corner of the inside of the gate, below we add the coordinates to a list
                coord_track.append([int(x_point), int(y_point)])
                # then draw the contours
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        #Do some logic if we only found 3 of the corners and we need the final corner
        if (len(coord_track) == 4):
            coord_track = sorted(coord_track, key = itemgetter(0))
            if (abs(coord_track[2][0]-coord_track[3][0])/abs(coord_track[0][0] - coord_track[1][0]) < .95 or abs(coord_track[2][0]-coord_track[3][0])/abs(coord_track[0][0] - coord_track[1][0]) > 1.05):
                    if (abs(coord_track[2][1]-coord_track[3][1])/abs(coord_track[0][1] - coord_track[1][1]) < .95 or abs(coord_track[2][1]-coord_track[3][1])/abs(coord_track[0][1] - coord_track[1][1]) > 1.05):
                            print("Failed")
        if (len(coord_track) == 3):
                #Find the average coordinate of the 3
                coord_sum = numpy.sum(coord_track,axis = 0)
                coord_avg = [int(round(coord_sum[0]/3)),int(round(coord_sum[1]/3))]
                #Find the nearest coordinate and remove it from the list
                coord_dist = []
                ct_copy = coord_track.copy()
                for i in coord_track:
                        coord_dist.append(numpy.sqrt(pow((i[0]-coord_avg[0]),2)+ pow((i[1]-coord_avg[1]),2)))
                del ct_copy[coord_dist.index(min(coord_dist))]
                #Use the x,y coordinates from the other 2 points based on their relative position to the average point
                if (abs(ct_copy[0][0]-coord_avg[0]) > abs(ct_copy[0][1]-coord_avg[1])):
                        coord_track.append([ct_copy[1][0],ct_copy[0][1]])
                else:
                        coord_track.append([ct_copy[0][0],ct_copy[1][1]])
                #Draw the points
        for x in coord_track:
                cv2.circle(image, (x[0],x[1]), 3, (213,32,246), -1, 8, 0)
#Go the hough line route
else:
        #Bench is just a blank image to draw the hough lines on, prolly easier way of doing this
        bench = cv2.imread('C:/Users/Sean Nemtzow/Documents/Fibinachos/blank.jpg')
        #Determine hough lines, draw on the blank image
        lines = cv2.HoughLinesP(detected, 1, numpy.pi / 180, 60, None, 10, 90)
        if lines is not None:
                for i in range(0, len(lines)):
                        l = lines[i][0]
                        difX = l[2] - l[0]
                        difY = l[3] - l[1]
                        cv2.line(bench, (int(round(l[0] - difX*.5)), int(round(l[1] - difY*.5))), (int(round(l[0] + difX*1.5)), int(round(l[1] + difY*1.5))), (0,0,0), 2, cv2.LINE_AA)
        #Draw a black rectangle aint(round the whole image to break up shapes
        cv2.rectangle(bench,(0,0),(799,532),(0,0,0), 7, 8)
        #Find the countours created by the hough lines
        gray_bench = cv2.cvtColor(bench, cv2.COLOR_BGR2GRAY)
        cnts_low = cv2.findContours(gray_bench, cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts_low = imutils.grab_contours(cnts_low)
        #Find the contour whose centroid is closest to the center
        final_cont = []
        closest = 541
        for c in cnts_low:
                #Approximate the contours to get close to rectangular in shape
                epsilon = cv2.arcLength(c,True)
                approx = cv2.approxPolyDP(c,0.09*epsilon,True)
                M = cv2.moments(approx)
                #Filter out contours whose area is too small or too big
                if (M["m00"] > 10 and M["m00"] < 400000):
                        Cx = M["m10"]/M["m00"]
                        Cy = M["m01"]/M["m00"]
                        distance = numpy.sqrt((int(400-Cx))**2 + (int(267-Cy))**2)
                        #Iterate through list, updating the contour who is closes to the center
                        if (distance < closest):
                                closest = distance
                                approx = approx.astype("float")
                                approx = approx*ratio
                                approx = approx.astype("int")
                                final_cont = [approx]
        #If we found one, draw a rectangle
        if(len(final_cont) > 0):
                x,y,w,h = cv2.boundingRect(final_cont[0])
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                coord_track = []
                coord_track = [[x,y],[x,y+h],[x+w,y],[x+w,x+h]]
        #If not, guess the middle
        else:
                dimY = image.shape[0]
                dimX = image.shape[1]
                centerX = math.ceil(dimX/2)
                centerY = math.ceil(dimY/2)
                x1 = int(centerX-(0.1*dimX))
                y1 = int(centerY - (0.1*dimX))
                x2 = int(centerX + (0.1*dimX))
                y2 = int(centerY + (0.1*dimX))
                cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0), 2)
                print("Note: No final contour, guessing middle")
#Show the final image
reformat = [[]]
for x in coord_track:
        for y in x:
                reformat[0].append(y)
                
print(reformat)
cv2.imshow(string, image)
#cv2.imwrite('Filtered_contours_2.jpg',image) #Uncomment this if you want to save the results
