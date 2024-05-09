# From: https://download.franka.de/opcua-server-doc-v2.0.4/developer_simpleClientPython.html
# Import dependencies
from opcua import Client, ua
from opcua.common.type_dictionary_buider import get_ua_class

# Configure and connect the client
client = Client("opc.tcp://<robot-ip>:4840/")  # 4840 is the default OPC UA port
client.set_user("<username>")  # Change to your user name ...
client.set_password("<password>")  # ... and password here
client.connect()  # Connect our client to the robot
typedefs = client.load_type_definitions()  # Load custom type definitions

# Browse the server
root = client.get_root_node()
robot = root.get_child("0:Objects").get_child("2:Robot")
keyPoseMapObject = robot.get_child("2:KeyValueMaps").get_child("2:KeyPoseMap")
setKeyPoseMethod = keyPoseMapObject.get_child("2:Replace")
getKeyPoseMethod = keyPoseMapObject.get_child("2:Read")

# Create a new Key-Pose-Pair
myKeyPosePair = get_ua_class("KeyPosePair")()
myKeyPosePair.Key = "test key"
myKeyPosePair.Value = [1.0, 0.0, 0.0, 0.0,
                       0.0, -1.0, 0.0, 0.0,
                       0.0, 0.0, -1.0, 0.0,
                       0.3, 0.0, 0.5, 1.0]

keyPoseMapObject.call_method(setKeyPoseMethod, ua.Variant(myKeyPosePair, ua.VariantType.ExtensionObject))
print(keyPoseMapObject.call_method(getKeyPoseMethod, "test key"))
