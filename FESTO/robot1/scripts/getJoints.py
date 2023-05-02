#!/usr/bin/env python3
import sys
import math
import rospy
import RV_3SDB
from geometry_msgs.msg import Point
from robot1.msg import jointMessage

import roslib
import math
import time
import os

path = os.getcwd() + '/src/RV_3SDB/src'
print(path)
sys.path.insert(0, path)


robot_location  = Point()
joint_location = jointMessage()

joint_location.j1 = 0.0
joint_location.j2 = 0.0
joint_location.j3 = 0.0
joint_location.j4 = 0.0
joint_location.j5 = 0.0
joint_location.j6 = 0.0
joint_location.j7 = 0.0
joint_location.speed = 0.0

TCP_IP = '10.1.1.110'
TCP_PORT = 10002
rv_3sdb_robot = RV_3SDB.RobotArm(TCP_IP, TCP_PORT)
#RV_3SDB = Communication(TCP_IP, TCP_PORT)

x = 0
y = 0



def moveRobot():
    global x, y, robot_location, joint_location

    if (x >= 100):
        x = 0
    else:
        x+=1

    if (y >= 100):
        y = 0
    else:
        y +=3
    robot_location.x = x
    robot_location.y = y


    #robot_Response = readJointPosition()
    #robot_joint_location = getJoints(robot_Response)
    robot_joint_location = rv_3sdb_robot.readJointPosition()
    print(robot_joint_location)
    joint_location.j1 = float(robot_joint_location.split(";")[1])
    joint_location.j2 = float(robot_joint_location.split(";")[3])
    joint_location.j3 = float(robot_joint_location.split(";")[5])
    joint_location.j4 = float(robot_joint_location.split(";")[7])
    joint_location.j5 = float(robot_joint_location.split(";")[9])
    joint_location.j6 = float(robot_joint_location.split(";")[11])
    #joint_location.j7 = float(robot_joint_location.split(";")[13])
    joint_location.speed = float(robot_joint_location.split(";")[16])

    


if __name__ == '__main__':
    robot_publisher = rospy.Publisher('rv_3sdb/showJointPosition', jointMessage, queue_size=10)
    rospy.init_node('rv_3sdb', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        moveRobot()
        robot_publisher.publish(joint_location)
        time.sleep(5)
