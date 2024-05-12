"""Small example OSC server
From: https://pypi.org/project/python-osc/
This program listens to /opacity address, and prints some information about
received packets.
"""
import argparse
import time

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from typing import List, Any

def nice_print(address: str, *osc_arguments: List[Any]):
    text = str(osc_arguments[0])
    print(f"Received message: {text[0:6]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=8020, help="The port to listen on")
    args = parser.parse_args()

    # Define which channel to listen to and which function to execute if a message is received
    dispatcher = Dispatcher()
    dispatcher.map("/opacity", nice_print)

    server = osc_server.BlockingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

    while True:
        server.handle_request()
