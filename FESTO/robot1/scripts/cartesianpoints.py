#!/usr/bin/env python3
import sys
import math
import rospy
import time
import os
import RV_3SDB
from robot1.msg import cartesianMessage

cartesian_points = cartesianMessage()

cartesian_points.X = 0.0
cartesian_points.Y = 0.0
cartesian_points.Z = 0.0
cartesian_points.A = 0.0
cartesian_points.B = 0.0
cartesian_points.C = 0.0
cartesian_points.L1 = 0.0
cartesian_points.speed = 0.0

TCP_IP = '10.1.1.110'
TCP_PORT = 10002
rv_3sdb_robot = RV_3SDB.RobotArm(TCP_IP, TCP_PORT)
def cartesian_update():
    global cartesian_points
    robot_cartesian_points = rv_3sdb_robot.readCartesianPosition()
    print (robot_cartesian_points)

    cartesian_points.X = float(robot_cartesian_points.split(";")[1])
    cartesian_points.Y = float(robot_cartesian_points.split(";")[3])
    cartesian_points.Z = float(robot_cartesian_points.split(";")[5])
    cartesian_points.A = float(robot_cartesian_points.split(";")[7])
    cartesian_points.B = float(robot_cartesian_points.split(";")[9])
    cartesian_points.C = float(robot_cartesian_points.split(";")[11])
    #cartesian_points.L1 = float(robot_cartesian_points.split(";")[13])
    cartesian_points.speed = float(robot_cartesian_points.split(";")[16])

if __name__ == '__main__':
    robot_publisher = rospy.Publisher('/showCartesianPoints', cartesianMessage, queue_size=10)
    rospy.init_node('rv_3sdb', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        cartesian_update()
        robot_publisher.publish(cartesian_points)
        time.sleep(5)