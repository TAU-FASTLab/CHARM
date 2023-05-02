import time
from communication import Communication

class RobotArm:

    def __init__(self, TCP_IP, TCP_PORT):
        self.RV_3SDB = Communication(TCP_IP, TCP_PORT)

    def reset(self):
        commands = []
        commands.append('CNTLOFF')
        commands.append('RSTALRM')
        commands.append('SRVOFF')
        commands.append('STATE')
        commands.append('CNTLON')
        return self.RV_3SDB.send(commands, commands)

    def servoOn(self):
        commands = []
        commands.append('OPEN=NARCUSR')
        commands.append('CNTLON')
        commands.append('SRVON')
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands, commands[2])[0]

    def servoOff(self):
        commands = []
        commands.append('CNTLON')
        commands.append('SRVOFF')
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands, commands[1])[0]

    def handOpen(self):
        commands = []
        commands.append('CNTLON')
        commands.append('EXECHOPEN 1')
        commands.append('CNTLOFF')
        #RV_3SDB.send(commands)
        return self.RV_3SDB.send(commands, commands[1])[0]

    def handClose(self):
        commands = []
        commands.append('CNTLON')
        commands.append('EXECHCLOSE 1')
        commands.append('CNTLOFF')
        # RV_3SDB.send(commands)
        return self.RV_3SDB.send(commands, commands[1])[0]

    def readJointPosition(self):
        commands = []
        commands.append('CNTLON')
        commands.append('JPOSF')
        commands.append('CNTLOFF')
        joint_msg = self.RV_3SDB.send(commands, ['JPOSF'])[0]
        return self.getJoints(joint_msg)

    def getJoints(self, robot_Response):
        print(robot_Response)
        joints_data = robot_Response[3:-1]
        joints_list = joints_data.split(";")
        joints_dict = {}
        index = 0
        for item in joints_list:
            index = joints_list.index(item)
            if item == "" or item == "***":
                break
            if index % 2 == 0:
                joints_dict[joints_list[index]] = float(joints_list[index + 1])
        joints_dict['speed'] = float(joints_list[16])
        print("--------------------------------", joints_dict['speed'])
        return joints_dict

    def readCartesianPosition(self):
        commands = []
        commands.append('CNTLON')
        commands.append('PPOSF')
        commands.append('CNTLOFF')
        cartezian_msg = self.RV_3SDB.send(commands, ['PPOSF'])[0]
        return self.getCartezian(cartezian_msg)

    def getCartezian(self, robot_Response):
        cartezian_data = robot_Response[3:-1]
        cartezian_list = cartezian_data.split(";")
        cartezian_dict = {}
        for item in cartezian_list:
            index = cartezian_list.index(item)
            if item == "":
                break
            if index % 2 == 0:
                cartezian_dict[cartezian_list[index]] = float(cartezian_list[index + 1])
        cartezian_dict['speed'] = cartezian_list[16]
        return cartezian_dict

    def moveJointPosition(self, j1, j2, j3, j4, j5, j6, j7, speed):
        jointPosition = self.jointPositionStringConstructor(j1, j2, j3, j4, j5, j6, j7)
        speedString = str(speed)

        commands = []
        commands.append('CNTLON')
        commands.append('EXECJOVRD ' + speedString)
        commands.append('EXECJCOSIROP = ' + jointPosition)
        commands.append('EXECMOV JCOSIROP')
        commands.append('CNTLOFF')
        response = self.RV_3SDB.send(commands, ['CNTLON', 'EXECJOVRD ' + speedString, 'EXECJCOSIROP = ' + jointPosition,
                                           'EXECMOV JCOSIROP'])
        if (response == ['QoK'] * 4):
            jointPositionDict = self.readJointPosition()
            while (jointPositionDict['J1'] != j1 or jointPositionDict['J2'] != j2 or
                   jointPositionDict['J3'] != j3 or jointPositionDict['J4'] != j4 or jointPositionDict['J5'] != j5
                   or jointPositionDict['J6'] != j6):
                time.sleep(1)
                jointPositionDict = self.readJointPosition()

        print(response)

    def jointPositionStringConstructor(self,j1, j2, j3, j4, j5, j6, j7):
        j1String = str(j1)
        j2String = str(j2)
        j3String = str(j3)
        j4String = str(j4)
        j5String = str(j5)
        j6String = str(j6)
        j7String = str(j7)

        jointPosition = '(' + j1String + ', ' + j2String + ', ' + j3String + ', ' + \
                        j4String + ', ' + j5String + ', ' + j6String + ', ' + j7String + ')'

        return jointPosition
