"""Small example OSC client

This example program asks for user input to send a message to a OSC channel
"""
import argparse
from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8010,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    print("The Server settings are: IP: ", args.ip, "   Port: ", args.port)

    while True:
        value = str(input("Add message you want to send in the format /channel;message\n"))
        # Example: /medias/Text_Generator/Text;test
        channel, text = value.split(";")
        client.send_message(channel, text)
