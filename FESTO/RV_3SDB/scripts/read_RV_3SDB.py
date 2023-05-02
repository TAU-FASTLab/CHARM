import time

from communication import Communication


TCP_IP = '153.1.165.72'
TCP_PORT = 10001

RV_3SDB = Communication(TCP_IP, TCP_PORT)

# commands = []
# commands.append('CNTLON')
# commands.append('STATE')
# commands.append('CNTLOFF')


def servoOn():
    commands = []
    commands.append('OPEN=NARCUSR')
    commands.append('CNTLON')
    commands.append('SRVON')
    commands.append('CNTLOFF')
    RV_3SDB.send(commands)


def servoOff():
    commands = []
    commands.append('CNTLON')
    commands.append('SRVOFF')
    commands.append('CNTLOFF')
    RV_3SDB.send(commands)

def handOpen():
    commands = []
    commands.append('CNTLON')
    commands.append('EXECHOPEN 1')
    commands.append('CNTLOFF')
    RV_3SDB.send(commands)


def handClose():
    commands = []
    commands.append('CNTLON')
    commands.append('EXECHCLOSE 1')
    commands.append('CNTLOFF')
    RV_3SDB.send(commands)


def readJointPosition():
    commands = []
    commands.append('CNTLON')
    commands.append('JPOSF')
    commands.append('CNTLOFF')
    return RV_3SDB.send(commands, ['JPOSF'])[0]


def readCartesianPosition():
    commands = []
    commands.append('CNTLON')
    commands.append('PPOSF')
    commands.append('CNTLOFF')
    RV_3SDB.send(commands, ['PPOSF'])


def jointPositionStringConstructor(j1, j2, j3, j4, j5, j6):
    j1String = str(j1)
    j2String = str(j2)
    j3String = str(j3)
    j4String = str(j4)
    j5String = str(j5)
    j6String = str(j6)

    jointPosition = '(' + j1String + ', ' + j2String + ', ' + j3String + ', ' +\
                    j4String + ', ' + j5String + ', ' + j6String + ')'

    return jointPosition


def moveJointPosition( j1, j2, j3, j4, j5, j6, speed):
    jointPosition = jointPositionStringConstructor(j1, j2, j3, j5, j4, j6)
    speedString = str(speed)

    commands = []
    commands.append('CNTLON')
    commands.append('EXECJOVRD ' + speedString)
    commands.append('EXECJCOSIROP = ' + jointPosition)
    commands.append('EXECMOV JCOSIROP')
    commands.append('CNTLOFF')
    response = RV_3SDB.send(commands, ['CNTLON', 'EXECJOVRD ' + speedString, 'EXECJCOSIROP = ' + jointPosition,
                              'EXECMOV JCOSIROP'])
    print(response)


    # Waits the robot reaches the joint position
    # jointPositionDict = self.stringHandler.getJointPositionByString(self.readJointPosition())
    # while (jointPositionDict["J1"] != j1 or jointPositionDict["J2"] != j2 or jointPositionDict["J3"] != j3 or
    #        jointPositionDict["J5"] != j5):
    #     time.sleep(0.2)
    #     jointPositionDict = self.stringHandler.getJointPositionByString(self.readJointPosition())

def getJoints(robot_Response):
    joints_data = robot_Response[3:-1]
    joints_list = joints_data.split(";")
    joints_dict = {}
    for item in joints_list:
        index = joints_list.index(item)
        if item == "":
            break
        if index % 2 == 0:
            joints_dict[joints_list[index]] = float(joints_list[index + 1])

    return joints_dict

if __name__ =='__main__':
    servoOn()
    time.sleep(5)
    moveJointPosition(10, -89.19, 169.39, 1.44, 2.6, -3.05, 5)
    while True:
        joints_response = readJointPosition()
        print(joints_response)
        joints_data = joints_response[3:-1]
        print(joints_data)
        joints_list = joints_data.split(";")
        print(joints_list)
        joints_dict = {}
        for item in joints_list:
            index = joints_list.index(item)
            if item == "":
                break
            if index % 2 == 0:
                joints_dict[joints_list[index]] = float(joints_list[index+1])

        print(joints_dict)
        #servoOff()
        print()
        time.sleep(5)
        #readCartesianPosition()

