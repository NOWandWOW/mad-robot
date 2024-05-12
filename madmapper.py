import time
from typing import List, Any
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher


def nice_print(address: str, fixed_argument: List[Any], *osc_arguments: List[Any]):
    text = str(osc_arguments[0])
    print(f"Received message: {text[0:6]}")
    print(f"{fixed_argument[0]}")

    
class MadMapper:
    def __init__(self, ip="127.0.0.1", port_in=8010, port_out=8030, logging="INFO"):
        self.IP = ip
        self.PORT_IN = port_in
        self.PORT_OUT = port_out
        self.log = logging
        self.client = udp_client.SimpleUDPClient(self.IP, self.PORT_IN)
        print(f"The Madmapper settings are: IP: {self.IP} and Inbound Port: {self.PORT_IN} and Outbound Port: {self.PORT_OUT}")
        self.dispatcher = Dispatcher()
        self.server = osc_server.ThreadingOSCUDPServer((self.IP, self.PORT_OUT), self.dispatcher)

    def send_message(self, channel, message):
        self.client.send_message(channel, message)

    def register_handler(self, address, handler, *args):
        self.dispatcher.map(address, handler, *args)

    def start_server(self):
        print(f"Serving on {self.server.server_address}")
        self.server.serve_forever()

    def handle_request(self):
        self.server.handle_request()

    def stop_server(self):
        self.server.shutdown()

    def __del__(self):
        self.stop_server()


if __name__ == "__main__":
    # Create an instance of MadMapper
    madmapper = MadMapper()

    # Register a handler
    madmapper.register_handler("/opacity", nice_print, "addtional argument")

    while True:
        # Handle the next request
        madmapper.handle_request() 

        # Send a message via OSC
        madmapper.send_message("/channel", "Hello!")
        time.sleep(0.1)