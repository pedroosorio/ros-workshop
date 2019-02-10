#!/usr/bin/env python

import os
import sys
import rospy
import uuid
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def camstream_node():
	node_name = "pycam_" + str(uuid.uuid4())
	node_name = node_name.replace("-", "_")
	rospy.init_node(node_name, anonymous=False)
	
	rospy.logwarn("Creating publisher node with the following name: '%s'" % node_name)
	
	# Create the subscriber
	wspub = rospy.Publisher("/workshop/webcam", Image, queue_size=1)
	# Use 'rqt_image_view /workshop/webcam' to view the image being transmitted
	
	bridge = CvBridge()
	camera = cv2.VideoCapture(-1)
	
	while not rospy.is_shutdown():
		#frame = cv2.imread(ros_logo,0)
		ret, frame = camera.read()
		# Publish the image after conversion
		cvimg = bridge.cv2_to_imgmsg(frame, "bgr8")
		wspub.publish(cvimg)
	###
			
	cv2.destroyAllWindows()
#####



if __name__ == '__main__':
	try:
		camstream_node()
	except rospy.ROSInterruptException:
		pass
#####
