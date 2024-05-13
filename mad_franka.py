import time
from madmapper import MadMapper
from robot import Robot

# Define variables
AUTH = "<ENTER COOKIE HERE>"
ROBOT_IP = "<ENTER ROBOT IP HERE>"
MAD_IP = "<ENTER MADMAPPER IP HERE>"
MAD_PORT_IN = 8010
MAD_PORT_OUT = 8030

robot = Robot(ROBOT_IP, cookie=AUTH)
madmapper = MadMapper(MAD_IP, MAD_PORT_IN, MAD_PORT_OUT)


def task_execution():
    robot.start_task("test")

def mode1():
    while True:
        pos = robot.get_position()
        pos_x = pos["cartesianPose"][0]
        pos_y = pos["cartesianPose"][2]

        madmapper.send_message("/medias/Text_Generator/Font/Text", f"x: {str(pos_x)[0:5]} ; y: {str(pos_y)[0:5]}")
        
        # DO some transformations with the robot position if needed
        trafo1 = -10.0 * (float(str(pos_x)[0:6])-0.63)
        print(trafo1)
        trafo2 = -5.0 * (float(str(pos_y)[0:6])-0.1)
        print(trafo2)
        madmapper.send_message("/surfaces/Quad-1/input/x", trafo1)
        madmapper.send_message("/surfaces/Quad-1/input/y", trafo2)
        
        time.sleep(0.05)

def mode2():
    # Define which OSC channels to listen to and which function to execute if a message is received
    madmapper.register_handler("/event", print)

    while True:
        madmapper.handle_request()
        time.sleep(0.1)


if __name__ == "__main__":
    # Login and Prepare Robot
    robot.prepare_robot()

    mode_select = input("Please choose which mode to run:\n 1: Robot poses are sent to Madmapper\n 2: Madmapper messages are sent to Robot\n")
    if mode_select == "1":
        mode1()
    elif mode_select == "2":
        mode2()
    else:
        print("Invalid mode selection")
        exit()