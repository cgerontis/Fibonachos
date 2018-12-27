#!/usr/bin/env python
import rospy as rsp
from sensor_msgs.msg import Image
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import math

class ZedCamPub:

	def __init__(self):
		self.bridge = CvBridge() #allows us to convert our image to cv2

		self.color_pub = rsp.Publisher("/exploring_challenge", String, queue_size=10 )#published a string saying the color of the detected blob
		self.zed_pub = rsp.Publisher("/image_echo", Image, queue_size=1)

		self.zed_img = rsp.Subscriber("/camera/rgb/image_rect_color", Image, self.detect_img) #subscribes to the ZED camera image

	      	self.odom_sub = rsp.Subscriber("/vesc/odom", Odometry, self.odom_callback)
		self.last_arb_position = Point()
		self.gone_far_enough = True

		self.heightThresh = 100 #unit pixels MUST TWEAK
		self.odomThresh = 1 #unit meters
		rsp.init_node("color_pub")

    	def odom_callback(self, odom): #odom callback
        	dist = math.sqrt((self.last_arb_position.x - odom.pose.pose.position.x)**2 + (self.last_arb_position.y - odom.pose.pose.position.y)**2)
        	if(dist > 1):#if moved a meter since last
        		self.gone_far_enough = True
        		self.last_arb_position.x = odom.pose.pose.position.x
        		self.last_arb_position.y = odom.pose.pose.position.y
        	else:
      			self.gone_far_enough = False

	def detect_img(self, img): #image callback
        	if(not self.gone_far_enough):
        		return

		img_data = self.bridge.imgmsg_to_cv2(img) #changing image to cv2

		processed_img_cv2 = self.process_img(img_data) #passing image to process_img function
		processed_img = self.bridge.cv2_to_imgmsg(processed_img_cv2, "bgr8") #convert image back to regular format (.png?)
        	cv2.imwrite("/home/racecar/challenge_photos/%i.png" % rsp.get_time(), processed_img_cv2)
		self.zed_pub.publish(processed_img)

	def process_img(self, img):
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #converting to HSV

		#GREEN
		hue_green_min = 60
		hue_green_max = 150

		sat_green_min = .5
		sat_green_max = 1

		val_green_min = .4
		val_green_max = 1

		green_bounds = np.array([hue_green_min / 2, int(sat_green_min * 255), int(val_green_min * 255)]), np.array([hue_green_max / 2, int(sat_green_max * 255), int(val_green_max * 255)])

		maskGreen = cv2.inRange(hsv, green_bounds[0], green_bounds[1])
		contours_green, hierarchy_green = cv2.findContours(maskGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		#RED
		hue_red_min = 200
		hue_red_max = 250

		sat_red_min = .85
		sat_red_max = 1

		val_red_min = .2
		val_red_max = .9

		red_bounds = np.array([hue_red_min / 2, int(sat_red_min * 255), int(val_red_min * 255)]), np.array([hue_red_max / 2, int(sat_red_max * 255), int(val_red_max * 255)])
		#red_bounds = np.array([0,190,200]), np.array([15, 255, 255])
	 	maskRed = cv2.inRange(hsv, red_bounds[0], red_bounds[1])
		contours_red, hierarchy_red = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		#YELLOW
		hue_yellow_min = 0
		hue_yellow_max = 360

		sat_yellow_min = 0.3
		sat_yellow_max = 1

		val_yellow_min = .745
		val_yellow_max = 1

		yellow_bounds = np.array([hue_yellow_min / 2, int(sat_yellow_min * 255), int(val_yellow_min * 255)]), np.array([hue_yellow_max / 2, int(sat_yellow_max * 255), int(val_yellow_max * 255)])

	 	maskYellow = cv2.inRange(hsv, yellow_bounds[0], yellow_bounds[1])
		contours_yellow, hierarchy_yellow = cv2.findContours(maskYellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        	#BLUE
		hue_blue_min = 0
		hue_blue_max = 30

		sat_blue_min = 0.4
		sat_blue_max = 1

		val_blue_min = 0
		val_blue_max = .5

		blue_bounds = np.array([hue_blue_min / 2, int(sat_blue_min * 255), int(val_blue_min * 255)]), np.array([hue_blue_max / 2, int(sat_blue_max * 255), int(val_blue_max * 255)])

	 	maskBlue = cv2.inRange(hsv, blue_bounds[0], blue_bounds[1])
		contours_blue, hierarchy_blue = cv2.findContours(maskBlue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                #cv2.drawContours(img, contours_red, -1, (120, 0, 0), 4)
        	contour_list = [contours_red, contours_green, contours_yellow, contours_blue]
        	string_list = ["red", "green", "yellow", "blue"]

		try:
            		for i in range(len(contour_list)):
             	 		if len(contour_list[i]) != 0:
                  			contArea = [(cv2.contourArea(c), (c) ) for c in contour_list[i]]
                  			contArea = sorted(contArea, reverse = True, key = lambda x: x[0])
					cont = contArea[0][1]
                  			M = cv2.moments(cont)

                                        x, y, w, h = cv2.boundingRect(cont)
					contour_height = h
                  			if  contour_height > self.heightThresh:

						print (string_list[i] , "found")
                      				self.color_pub.publish(string_list[i])
                      				cv2.drawContours(img, cont, -1, (255, 255, 255), 10)

                      				if M['m00'] != 0:
		                  			cx = int(M['m10']/M['m00'])
		                  			cy = int(M['m01']/M['m00'])

		                  			center = (cx, cy)
		                  			cv2.circle(img, center, 5, (60, 0, 0), -1)
		                  			#rect

		                  			cv2.rectangle(img, (x, y), (x + w, y + h), (100, 50, 50), 2)

		                  			font = cv2.FONT_HERSHEY_SIMPLEX
		                  			cv2.putText(img, string_list[i], center, font, 1,(0,0,0) , 4)

		except Exception, e:
			print str(e)


		return img

if __name__ == "__main__":
	node = ZedCamPub()
	rsp.spin()
