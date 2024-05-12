import requests
import json
import inspect

def send_get_request(url, headers=None, params=None, auth=None):
    """Sends a GET request to the specified URL."""
    headers = add_base_header(headers, auth)
    response = requests.get(url, headers=headers, params=params)
    return response

def send_post_request(url, headers=None, data=None, auth=None):
    """Sends a POST request to the specified URL."""
    headers = add_base_header(headers, auth)
    response = requests.post(url, headers=headers, data=data)
    return response

def add_base_header(headers, auth):
    base_header = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": f"authorization={auth}"}
    headers = headers or {}
    headers.update(base_header)
    return headers

def process_response(response, log_level="INFO"):
    """Check if the response is successful and return parsed JSON."""
    calling_function = inspect.currentframe().f_back.f_code.co_name
    if response.status_code == 200:
        if log_level == "DEBUG":
            print(f"{calling_function.upper()} succeeded")
        return json.loads(response.text)
    else:
        print(f"{calling_function.upper()} FAILED with status code {response.status_code}")
        return None