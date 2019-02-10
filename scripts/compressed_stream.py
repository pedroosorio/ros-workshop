#!/usr/bin/env python

import os
import sys
import rospy
import uuid
import cv2
import numpy as np

from sensor_msgs.msg import CompressedImage
from workshop.srv import cannycontrol
from workshop.srv import cannycontrolResponse

canny = True
t1 = 100
t2 = 200
camera = None
wspub = None
cannyserv = None

def publish_compressed_image(event):
	global t1, t2, camera, wspub, canny
	ret, frame = camera.read()
	if ret == False:
		return
	if canny:
		frame = cv2.Canny(frame,t1,t2)

	msg = CompressedImage()
	msg.header.stamp = rospy.Time.now()
	msg.format = "png"
	msg.data = np.array(cv2.imencode('.png', frame)[1]).tostring()

	wspub.publish(msg)
#####

def handle_canny_control(request):
	global t1, t2, camera, wspub, canny
	output = "ERROR: UNKNOWN PARAM"
	if request.param.lower() == "state":
		canny = True if request.value > 0 else False
		keyword = "ON" if canny == True else "OFF"
		output = "Canny is now %s" % keyword
	if request.param.lower() == "t1":
		t1 = request.value
		output = "T1 is now %d" % t1
	if request.param.lower() == "t2":
		t2 = request.value
		output = "T2 is now %d" % t2
	return cannycontrolResponse(output)
#####


def compressstream_node():
	global t1, t2, camera, wspub, canny
	node_name = "pycompressed_" + str(uuid.uuid4())
	node_name = node_name.replace("-", "_")
	rospy.init_node(node_name, anonymous=False)
	
	rospy.logwarn("Creating publisher node with the following name: '%s'" % node_name)
	
	# Create the subscriber
	wspub = rospy.Publisher("/workshop/compressed", CompressedImage, queue_size=1)
	# Use 'rqt_image_view /workshop/webcam' to view the image being transmitted
	s = rospy.Service('/workshop/CannyCtrl', cannycontrol, handle_canny_control)
	
	camera = cv2.VideoCapture(-1)
	
	timer = rospy.Timer(rospy.Duration(0.06), publish_compressed_image)
    	rospy.spin() 
			
	cv2.destroyAllWindows()
#####



if __name__ == '__main__':
	try:
		compressstream_node()
	except rospy.ROSInterruptException:
		pass
#####
