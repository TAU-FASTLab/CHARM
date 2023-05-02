#!/usr/bin/env python3
import sys
import math
import rospy
from RV_3SDB.msg import jointMessage
from geometry_msgs.msg import Point
import roslib
import math
import time
import os

path = os.getcwd() + '/src/RV_3SDB/src'
print(path)
sys.path.insert(0, path)
#from communication import Communication
from RV_3SDB_Robot import RobotArm
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
TCP_PORT = 10001
rv_3sdb_robot = RobotArm(TCP_IP, TCP_PORT)
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
    joint_location.j1 = robot_joint_location['J1']
    joint_location.j2 = robot_joint_location['J2']
    joint_location.j3 = robot_joint_location['J3']
    joint_location.j4 = robot_joint_location['J4']
    joint_location.j5 = robot_joint_location['J5']
    joint_location.j6 = robot_joint_location['J6']
    joint_location.j7 = robot_joint_location['J7']
    joint_location.speed = robot_joint_location['speed']

    


if __name__ == '__main__':
    robot_publisher = rospy.Publisher('rv_3sdb/showJointPosition', jointMessage, queue_size=10)
    rospy.init_node('rv_3sdb', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        moveRobot()
        robot_publisher.publish(joint_location)
        time.sleep(5)
