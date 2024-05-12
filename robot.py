from utils import process_response, send_get_request, send_post_request, add_base_header

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
        response = send_get_request(url)
        # Process the response and return the position
        return process_response(response, log_level=self.log)

    def get_robot_status(self):
        # Send a GET request to retrieve the robot's status
        url = f"{self.base_url}/robot/status"
        response = send_get_request(url)
        # Process the response and return the status
        return process_response(response, log_level=self.log)

    def get_system_status(self):
        # Send a GET request to retrieve the robot's status
        url = f"{self.base_url}/system/status"
        response = send_get_request(url)
        # Process the response and return the status
        return process_response(response, log_level=self.log)

    def open_brakes(self):
        # Send a POST request to open the robot's brakes
        url = f"{self.base_url}/robot/open-brakes"
        data = {"force": "false"}
        response = send_post_request(url, data=data)
        return process_response(response, log_level=self.log)

    def close_brakes(self):
        # Send a POST request to close the robot's brakes
        url = f"{self.base_url}/robot/close-brakes"
        response = send_post_request(url)
        return process_response(response, log_level=self.log)

    def start_task(self, task_name):
        url = f"{self.base_url}/execution"
        data = {"id": f"0_{task_name}"}
        response = send_post_request(url, data=data)
        # Process the response as needed
        return process_response(response, log_level=self.log)
    
    def login_robot(self):
        # Send a POST request to login to the robot
        url = f"https://{self.IP}/admin/api/login"
        data = {"login": f"{self.user}", "password": f"{self.password}"}
        response = send_post_request(url, data=data)
        # Process the response as needed
        return process_response(response, log_level=self.log)

    def prepare_robot(self):
        # Perform necessary steps to prepare the robot
        self.login_robot()
        self.open_brakes()

       
if __name__ == "__main__":
    ROBOT_IP = "192.168.1.13"
    robot = Robot(ROBOT_IP)

    while True:
        number = int(input("\n\nPlease enter a number from 1 to 8, with the following actions to happen: \
                   \n1: Login to the robot \
                   \n2: Open the brakes \
                   \n3: Close the brakes \
                   \n4: Get the robot status \
                   \n5: Get the system status \
                   \n6: Get the robot position \
                   \n7: Prepare the robot \
                   \n8: Start the task 'test'\n"))
        
        switcher = {
            1: robot.login_robot(),
            2: robot.open_brakes(),
            3: robot.close_brakes(),
            4: robot.get_robot_status(),
            5: robot.get_system_status(),
            6: robot.get_position(),
            7: robot.prepare_robot(),
            8: robot.start_task("test")
        }

        # Get the function based on the input number
        selected_function = switcher.get(number)

        # Call the selected function if it exists
        if selected_function:
            selected_function()
        else:
            print("Invalid number")
