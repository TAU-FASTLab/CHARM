import time

from communication import Communication
TCP_IP = '10.1.1.110'
TCP_PORT = 10002

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
        return self.RV_3SDB.send(commands)
          
    def servoOn(self):
        commands = []
        commands.append('OPEN=NARCUSR')
        commands.append('CNTLON')
        commands.append('SRVON')
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands)

    def servoOff(self):
        commands = []
        commands.append('CNTLON')
        commands.append('SRVOFF')
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands)

    def handOpen(self):
        commands = []
        commands.append('CNTLON')
        commands.append('EXECHOPEN 1')
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands)


    def handClose(self):
        commands = []
        commands.append('CNTLON')
        commands.append('EXECHCLOSE 1')
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands)

    def setSpeed(self):
        commands = []
        commands.append('CNTLON')
        speed = input("Enter the Speed: ")
        commands.append('OVRD='+ str(speed))
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands)

    def runProgram(self):
        commands = []
        commands.append('CNTLON')
        commands.append('SRVON')
        program_name = str(input("Enter the Program Name: "))
        commands.append('RUN'+ program_name + ';1')
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands)

    def loadProgram(self):
        commands = []
        commands.append('CNTLON')
        commands.append('SRVON')
        program_name = str(input("Enter the Program Name: "))
        commands.append('PRGLOAD='+ program_name)
        commands.append('EXECMOV J03')
        commands.append('CNTLOFF')
        print (self.RV_3SDB.send(commands))

    def safePosition(self):
        commands = []
        commands.append('CNTLON')
        commands.append('SRVON')
        commands.append('MOVSP')
        commands.append('CNTLOFF')
        return self.RV_3SDB.send(commands)

    def readJointPosition(self):
        commands = []
        commands.append('CNTLON')
        commands.append('JPOSF')
        commands.append('CNTLOFF')
        self.joints = self.RV_3SDB.send(commands, ['JPOSF'])[0]
        print(self.joints)
        return self.joints
    
    def readCartesianPosition(self):
        commands = []
        commands.append('CNTLON')
        commands.append('PPOSF')
        commands.append('CNTLOFF')
        cartesian_position = self.RV_3SDB.send(commands, ['PPOSF'])
        print(cartesian_position[0])
        return cartesian_position[0]


    def joint_format(self, response):

        #print(self.response.split(";"))
        # Split the self.response string on semicolons and extract the J2, J3, J4, J5, and J6 values
        j1_value = float(response.split(";")[1])
        j2_value = float(response.split(";")[3])
        j3_value = float(response.split(";")[5])
        j4_value = float(response.split(";")[7])
        j5_value = float(response.split(";")[9])
        j6_value = float(response.split(";")[11])
        j7_value = float(response.split(";")[13])
        speed = float(response.split(";")[16])

        # Print the J2, J3, J4, J5, and J6 values in the specified format
        print(f"J1 = {j1_value:.2f}")
        print(f"J2 = {j2_value:.2f}")
        print(f"J3 = {j3_value:.2f}")
        print(f"J4 = {j4_value:.2f}")
        print(f"J5 = {j5_value:.2f}")
        print(f"J6 = {j6_value:.2f}")
        print(f"J7 = {j7_value:.2f}")
        print(f"Speed = {speed:.2f}")

    def cartesian_format(self, response):

        #print(self.response.split(";"))
        # Split the self.response string on semicolons and extract the J2, J3, J4, J5, and J6 values
        X_value = float(response.split(";")[1])
        Y_value = float(response.split(";")[3])
        Z_value = float(response.split(";")[5])
        A_value = float(response.split(";")[7])
        B_value = float(response.split(";")[9])
        C_value = float(response.split(";")[11])
        L1_value = float(response.split(";")[13])
        speed = float(response.split(";")[16])

        # Print the J2, J3, J4, J5, and J6 values in the specified format
        print(f"X = {X_value:.2f}")
        print(f"Y = {Y_value:.2f}")
        print(f"Z = {Z_value:.2f}")
        print(f"A = {A_value:.2f}")
        print(f"B = {B_value:.2f}")
        print(f"C = {C_value:.2f}")
        print(f"L1 = {L1_value:.2f}")
        print(f"Speed = {speed:.2f}")
        


   



# if __name__ =='_main_':
#     #connect_robot('153.1.165.72', 10001)
#     # reset()
#     RobotArm()
#     RobotArm.servoOn
#     #runProgram()
#     #safePosition()
    
#     #servoOff()
#     #setSpeed()
#     #readCartesianPosition()
#     #readJointPosition()
#     #loadProgram()
#     #runProgram()
#     #loadProgram()
#     while True:
#         #cartesian_format(readCartesianPosition())
#         readJointPosition()
        
        
#         print("------------------------------------------------")
        
#         readCartesianPosition()
#         #joint_format(readJointPosition())
#         print("------------------------------------------------")
#         time.sleep(5)
   
#     #joint_format(readJointPosition())