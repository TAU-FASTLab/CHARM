import RV_3SDB
import time


TCP_IP = '153.1.165.72'
TCP_PORT = 10002
robot = RV_3SDB.RobotArm(TCP_IP, TCP_PORT)

#robot.servoOn()
robot.servoOff()
while True:
    Cartesian = robot.readCartesianPosition()
    Joints = robot.readJointPosition()
    robot.cartesian_format(Cartesian)
    robot.joint_format(Joints)
    time.sleep(5)

