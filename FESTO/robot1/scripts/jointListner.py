#!/usr/bin/env python3
import os
import rospy
from robot1.msg import jointMessage

import RV_3SDB      

TCP_IP = '10.1.1.110'
TCP_PORT = 10002



rv_3sdb_robot = RV_3SDB.RobotArm(TCP_IP, TCP_PORT)


def callback(data):
    rospy.loginfo(" I heard %s", data)
    print("Listening.....")

    #rv_3sdb_robot.moveJointPosition(data.j1, data.j2, data.j3, data.j4, data.j5, data.j6, data.j7, data.speed)
    print(data)


def listener():
    rv_3sdb_robot.servoOn()

    rospy.init_node('listenerJoint', anonymous=False)
    rospy.Subscriber("rv_3sdb/showJointPosition", jointMessage, callback)
    rospy.spin()

    #rv_3sdb_robot.servoOff()


if __name__ == '__main__':
    
    listener()
