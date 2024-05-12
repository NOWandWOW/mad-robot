import time
from madmapper import MadMapper
from robot import Robot

# Define variables
ROBOT_IP = "192.168.1.13"
MAD_IP = "127.0.0.1"
MAD_PORT_IN = 8010
MAD_PORT_OUT = 8030

robot = Robot(ROBOT_IP)
madmapper = MadMapper()


def task_execution():
    robot.start_task("test2")

def mode1():
    pos = robot.get_position()
    pos_x = pos["cartesianPose"][0]
    
    # DO some transformations with the robot position if needed
    madmapper.send_message("/channel", pos_x) 

def mode2():
    # Define which OSC channels to listen to and which function to execute if a message is received
    madmapper.register_handler("/execute/task", task_execution)

    while True:
        madmapper.handle_request()
        time.sleep(0.1)


if __name__ == "__main__":
    # Login and Prepare Robot
    robot.login_robot()
    robot.prepare_robot()

    mode_select = input("Please choose which mode to run:\n 1: Robot poses are sent to Madmapper\n 2: Madmapper messages are sent to Robot\n")
    if mode_select == "1":
        mode1()
    elif mode_select == "2":
        mode2()
    else:
        print("Invalid mode selection")
        exit()