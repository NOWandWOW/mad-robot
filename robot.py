from utils import process_response, send_get_request, send_post_request, add_base_header
import json
import requests


class Robot:
    def __init__(self, ip, user="", password="", cookie="", logging="INFO"):
        self.IP = ip
        self.base_url = f"https://{self.IP}/desk/api"
        self.user = user
        self.password = password
        self.AUTH_TOKEN = cookie
        self.log = logging

    def get_position(self):
        url = f"{self.base_url}/robot/configuration"
        response = send_get_request(url, auth=self.AUTH_TOKEN)
        # Process the response and return the position
        return process_response(response, log_level=self.log)

    def get_robot_status(self):
        # Send a GET request to retrieve the robot's status
        url = f"{self.base_url}/robot/status"
        response = send_get_request(url, auth=self.AUTH_TOKEN)
        # Process the response and return the status
        return process_response(response, log_level=self.log)

    def get_system_status(self):
        # Send a GET request to retrieve the robot's status
        url = f"{self.base_url}/system/status"
        response = send_get_request(url, auth=self.AUTH_TOKEN)
        # Process the response and return the status
        return process_response(response, log_level=self.log)
    
    def get_task_list(self):
        # Send a GET request to retrieve the robot's status
        url = f"{self.base_url}/timelines"
        response = send_get_request(url, auth=self.AUTH_TOKEN)
        # Process the response and return the status
        processed_response = process_response(response, log_level=self.log)
        task_names = []
        for i in range(len(processed_response)):
            task_names.append(processed_response[i]['id'])
        print(task_names)
        return task_names

    def open_brakes(self):
        # Send a POST request to open the robot's brakes
        url = f"{self.base_url}/robot/open-brakes"
        data = {"force": "false"}
        response = send_post_request(url, data=data, auth=self.AUTH_TOKEN)
        return process_response(response, log_level=self.log)

    def close_brakes(self):
        # Send a POST request to close the robot's brakes
        url = f"{self.base_url}/robot/close-brakes"
        response = send_post_request(url, auth=self.AUTH_TOKEN)
        return process_response(response, log_level=self.log)

    def start_task(self, task_name):
        url = f"{self.base_url}/execution"
        data = {"id": f"0_{task_name}"}
        response = send_post_request(url, data=data, auth=self.AUTH_TOKEN)
        # Process the response as needed
        return process_response(response, log_level=self.log)
    
    def create_task(self, task_name, body):
        url = f"{self.base_url}/timelines"
        payload = json.dumps(body)
        base_header = {"Content-Type": "application/json", "Cookie": self.AUTH_TOKEN, "X-Control-Token": "Da119rLfdMM/29Wuw5rFGz81uv7QJLkWEaIT3t+pduo="}
        headers = {}
        headers.update(base_header)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        # Process the response as needed
        return process_response(response, log_level=self.log)
    
    def UI_create_task(self):
        task_name = input("Choose a unique task name\n")
        f = open('task_template.json')
        body = json.load(f)
        
        body['parameter']['poses'][0]['relative_trajectories'][0]=[]
        body["id"] = "0_"+task_name
        body["name"] = task_name
        body['containers'][0]['elements'][0]['componentProviders']['motion']['componentLookupTable'][0]['sourcePath']['id'] = task_name

        num = input("How many points you want to teach?")
        for i in range(int(num)):
            val = input(f"please move to postition {i+1}:")
            pose = robot.get_position()
            print(pose)
        
            body['parameter']['poses'][0]['relative_trajectories'][0].append({'joint_angles':pose["jointAngles"], 'pose':pose["cartesianPose"]})

        self.create_task(task_name, body)
    
    def login_robot(self):
        # Send a POST request to login to the robot
        url = f"https://{self.IP}/admin/api/login"
        data = {"login": f"{self.user}", "password": f"{self.password}"}
        response = send_post_request(url, data=data, auth=self.AUTH_TOKEN)
        # Process the response as needed
        return process_response(response, log_level=self.log)

    def prepare_robot(self):
        # Perform necessary steps to prepare the robot
        self.open_brakes()

       
if __name__ == "__main__":
    ROBOT_IP = "192.168.1.195"
    AUTH = "authorization=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZnJhIiwicm9sZSI6eyJhdXRob3JpemF0aW9uIjpbeyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJUYXNrcyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiU2tpbGxzIn0seyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJQYXJhbWV0ZXJzIn0seyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJFeGVjdXRpb24ifSx7InBlcm1pc3Npb24iOiJSZWFkV3JpdGUiLCJyZXNvdXJjZSI6IlN0YXR1cyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiQnVuZGxlcyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiU2NyaXB0cyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiQWRtaW4ifSx7InBlcm1pc3Npb24iOiJSZWFkV3JpdGUiLCJyZXNvdXJjZSI6IlNhZmV0eSJ9XSwibmFtZSI6ImFkbWluIn19.rGp0QvF1_d96hbWbetPr4Eg7DVJ4drO8cz8bpUqONj17_LkezZSakqZ72u3gXjXaInA6OM97m-bu4thgFdgblw"
    robot = Robot(ROBOT_IP, cookie=AUTH, logging="INFO")

    while True:
        number = int(input("\n\nPlease enter a number from 1 to 7, with the following actions to happen: \
                   \n1: Open the brakes \
                   \n2: Close the brakes \
                   \n3: Get the robot position \
                   \n4: Get the robot status \
                   \n5: Get the system status \
                   \n6: Start the task 'matthieu'. CAREFUL the robot will move! \
                   \n7: Create new task \
                   \n8: Get Task List\n"))
        
        switcher = {
            1: robot.open_brakes,
            2: robot.close_brakes,
            3: robot.get_position,
            4: robot.get_robot_status,
            5: robot.get_system_status,
            6: robot.start_task, 
            7: robot.UI_create_task,
            8: robot.get_task_list
        }

        # Get the function based on the input number
        selected_function = switcher.get(number)

        # Call the selected function if it exists
        if selected_function == robot.start_task:
            val = selected_function("matthieu")
        elif selected_function:
            val = selected_function()
        else:
            print("Invalid number")
