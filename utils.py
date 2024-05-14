import requests
import json
import inspect
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_get_request(url, headers=None, params=None, auth=None):
    """Sends a GET request to the specified URL."""
    headers = add_base_header(headers, auth)
    response = requests.get(url, headers=headers, params=params, verify=False)
    return response

def send_post_request(url, headers=None, data=None, auth=None):
    """Sends a POST request to the specified URL."""
    headers = add_base_header(headers, auth)
    response = requests.post(url, headers=headers, data=data, verify=False)
    return response

def add_base_header(headers, auth):
    base_header = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": f"{auth}", "X-Control-Token": "Da119rLfdMM/29Wuw5rFGz81uv7QJLkWEaIT3t+pduo="}
    headers = headers or {}
    headers.update(base_header)
    return headers

def process_response(response, log_level="INFO"):
    """Check if the response is successful and return parsed JSON."""
    calling_function = inspect.currentframe().f_back.f_code.co_name
    if response.status_code == 200:
        parsed_response = json.loads(response.text or 'null')
        if log_level == "DEBUG":
            print(f"{calling_function.upper()} succeeded")
            print(parsed_response)
        return parsed_response
    else:
        print(f"{calling_function.upper()} FAILED with status code {response.status_code}")
        return None