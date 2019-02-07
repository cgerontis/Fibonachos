##coordinates.py takes a path to a folder and iterates through the images in that folder.
##For each image the user chooses coordinates on the image that
##they want to save. The left mouse button saves a coordinate
##and places a red circle, the 'd' key removes the last coordinate,
##and the 'c' key saves the coordinates and moves on to the next image.
##It saves the coordinates per line per image in coordinatesList.txt

# import necessary packages
import cv2
from os import listdir
from os.path import isfile, join
#initialize the list of coordinates
coordList = []


def fourclicks (event, x, y, flags, param):
    #Function fourclicks waits for the left mouse click, saves the coordinates, and draws a circle
    global coordList

    #if left mouse button was clicked, record the coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
            coordList.append((x, y))
            cv2.circle(image, (x, y), 3, (0,0,255), thickness = 1, lineType=8,shift=0)
            
#Create list of files in path given
path = input("Enter the path to the folder: ")
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
#Strip any files that don't end in .jpg, prolly an easier way to do this idk
for x in onlyfiles:
    if (x[-4:] != '.jpg'):
        onlyfiles.remove(x)
#print(onlyfiles) //Uncomment for problem solving
f = open("coordinateList.txt","a+")
#Iterate through the files
for x in onlyfiles:
    #print(x) //Uncomment for problem solving
    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread(path+'\\'+x)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", fourclicks)
     
    # keep looping until the 'c' key is pressed
    while True:
            # display the image and wait for a keypress
            cv2.imshow("image", image)
            key = cv2.waitKey(1) & 0xFF
     
            # if the 'd' key is pressed, remove the last coordinate
            if key == ord("d"):
                if len(coordList) > 0:
                    del coordList[-1:]
                    image = clone.copy()
                    for x in coordList:
                        cv2.circle(image, x, 3, (0,0,255), thickness = 1, lineType=8,shift=0)
                     
            # if the 'c' key is pressed, move on to the next image
            elif key == ord("c"):
                print(coordList)
                for x in coordList:
                    f.write("{0},".format(x))
                f.write("\n")
                coordList = []
                break
    cv2.destroyAllWindows()
    
f.close()
    
        
