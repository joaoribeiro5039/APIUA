from opcua import ua, Server
import json
import time
import random
import datetime

# create server
server = Server()
server.name = "SimpleOPCUA"
server.set_endpoint("opc.tcp://192.168.1.242:4840")

# create objects and variables from json file
with open("nodes.json", "r") as f:
    nodes = json.load(f)


for node in nodes:
    obj = server.nodes.objects.add_object(node["node_id"], node["name"])
    for var in node["variables"]:
        obj.add_variable(var["node_id"], var["name"], var["value"])
        obj.set_writable(True)
        obj.set_access_level(ua.AccessLevel.CurrentReadOrWrite)
        obj.set_user_access_level(ua.AccessLevel.CurrentReadAndWrite)

# start server
server.start()

try:
    while True:
        time.sleep(0.01)
        for node in nodes:
            for var in node["variables"]:
                if var["isRandom"]:
                    value = random.randint(var["range_min"], var["range_max"])
                    var_node = server.get_node(var["node_id"])
                    var_node.set_value(value)

finally:
    server.stop()