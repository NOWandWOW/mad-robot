import time
from madmapper import MadMapper
from robot import Robot

# Define variables
AUTH1 = "authorization=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZnJhIiwicm9sZSI6eyJhdXRob3JpemF0aW9uIjpbeyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJUYXNrcyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiU2tpbGxzIn0seyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJQYXJhbWV0ZXJzIn0seyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJFeGVjdXRpb24ifSx7InBlcm1pc3Npb24iOiJSZWFkV3JpdGUiLCJyZXNvdXJjZSI6IlN0YXR1cyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiQnVuZGxlcyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiU2NyaXB0cyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiQWRtaW4ifSx7InBlcm1pc3Npb24iOiJSZWFkV3JpdGUiLCJyZXNvdXJjZSI6IlNhZmV0eSJ9XSwibmFtZSI6ImFkbWluIn19.rGp0QvF1_d96hbWbetPr4Eg7DVJ4drO8cz8bpUqONj17_LkezZSakqZ72u3gXjXaInA6OM97m-bu4thgFdgblw"
AUTH2 = "authorization=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZnJhIiwicm9sZSI6eyJhdXRob3JpemF0aW9uIjpbeyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJUYXNrcyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiU2tpbGxzIn0seyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJQYXJhbWV0ZXJzIn0seyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJFeGVjdXRpb24ifSx7InBlcm1pc3Npb24iOiJSZWFkV3JpdGUiLCJyZXNvdXJjZSI6IlN0YXR1cyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiQnVuZGxlcyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiU2NyaXB0cyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiQWRtaW4ifSx7InBlcm1pc3Npb24iOiJSZWFkV3JpdGUiLCJyZXNvdXJjZSI6IlNhZmV0eSJ9XSwibmFtZSI6ImFkbWluIn19.uEjEaxuAhgtjVYSWbeCTBqXiGPoj6R8NQYIQSe5GpPX1oZt9H3d3LM-LiDCddLnkUvtcrI2dQMDtcYwQysCk2w"

XCONTROL1 = "q4ZspA4bhSlA9C9kS3Y0JYEqdnmDqIlZwcPFdE1gMJ8="
XCONTROL2 = "qXToB9Z/tr3zBI7R0Z83kAkxI8h4mM1rXeOppqrN9as="

ROBOT_IP1 = "192.168.1.195"
ROBOT_IP2 = "192.168.1.196"

MAD_IP = "<ENTER MADMAPPER IP HERE>"
MAD_PORT_IN = 8010
MAD_PORT_OUT = 8030

robot1 = Robot(ROBOT_IP1, cookie=AUTH1, xcontrol=XCONTROL1)
robot2= Robot(ROBOT_IP2, cookie=AUTH2, xcontrol=XCONTROL2)

#madmapper = MadMapper(MAD_IP, MAD_PORT_IN, MAD_PORT_OUT)


if __name__ == "__main__":
    robot1.open_brakes()
    robot2.open_brakes()

