#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 08:02:13 2015

@author: Chris
"""

import rospy
import tf
import tf_conversions.posemath as pm
from geometry_msgs.msg import PoseArray

last_pose = None

def callback(msg):
    if len(msg.poses) > 0:
        global last_pose
        last_pose = msg.poses[0]
        
if __name__ == '__main__':
    rospy.init_node('posearray_tf_republisher')
    
    sub = rospy.Subscriber('poses_out',PoseArray,callback)

    br = tf.TransformBroadcaster()
    try:
        rate = rospy.Rate(10)    
        while not rospy.is_shutdown():
            if not (last_pose is None):
                (trans, rot) = pm.toTf(pm.fromMsg(last_pose))
                br.sendTransform(trans, rot, rospy.Time.now(), 'drill', 'world')
            rate.sleep()
    except rospy.ROSInterruptException, e:
        print e
