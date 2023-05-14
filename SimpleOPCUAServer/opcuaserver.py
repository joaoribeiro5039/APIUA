from opcua import ua, Server
import json
import time
import random

# create server
server = Server()
server.set_endpoint("opc.tcp://127.0.0.1:4840")

# create objects and variables from json file
with open("nodes.json", "r") as f:
    nodes = json.load(f)

for node in nodes:
    obj = server.nodes.objects.add_object(node["node_id"], node["name"])
    for var in node["variables"]:
        obj.add_variable(var["node_id"], var["name"], var["value"])

# start server
server.start()

try:
    while True:
        time.sleep(0.5)
        for node in nodes:
            for var in node["variables"]:
                value = random.randint(var["range_min"], var["range_max"])
                var_node = server.get_node(var["node_id"])
                var_node.set_value(value)
finally:
    server.stop()