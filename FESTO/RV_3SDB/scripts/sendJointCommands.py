#!/usr/bin/env python3
import os
import rospy
path = os.getcwd() + '/src/RV_3SDB/src'
import sys
from RV_3SDB.msg import jointMessage

sys.path.insert(0, path)

import RV_3SDB_Robot

TCP_IP = '10.1.1.110'
TCP_PORT = 10001

rv_3sdb_robot = RV_3SDB_Robot.RobotArm(TCP_IP, TCP_PORT)


def callback(data):
    rospy.loginfo(" I heard %s", data)

    rv_3sdb_robot.moveJointPosition(data.j1, data.j2, data.j3, data.j4, data.j5, data.j6, data.j7, data.speed)
    print(data)


def listener():
    rv_3sdb_robot.servoOn()

    rospy.init_node('listenerJoint', anonymous=False)
    rospy.Subscriber("jointMovement", jointMessage, callback, queue_size=1000)
    rospy.spin()

    rv_3sdb_robot.servoOff()


if __name__ == '__main__':
    listener()
