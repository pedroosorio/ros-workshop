#!/usr/bin/env python

import sys
import rospy
import uuid
from workshop.msg import testmsg

def testmsg_callback(data):
	#rospy.logwarn("Received data")
	print("Recevied testmg from '%s' at [%d] -> '%s'" \
	% (data.sender, data.timestamp, data.msg))
#####


def sub_node():
	node_name = "pysub_" + str(uuid.uuid4())
	node_name = node_name.replace("-", "_")
	rospy.init_node(node_name, anonymous=False)
	
	rospy.logwarn("Creating publisher node with the following name: '%s'" % node_name)
	
	# Create the subscriber
	wssub = rospy.Subscriber("/workshop/chatter", testmsg, testmsg_callback)
	
	# Keep python instance running until the node dies
	rospy.spin()
#####



if __name__ == '__main__':
	try:
		sub_node()
	except rospy.ROSInterruptException:
		pass
	except:
		print("Unexpected error: %s" % sys.exc_info()[0])
#####
