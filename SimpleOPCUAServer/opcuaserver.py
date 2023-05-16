from opcua import ua, Server
import time
import random
import datetime
import json

# create server
server = Server()
server.name = "SimpleOPCUA"
server.set_endpoint("opc.tcp://0.0.0.0:4840")

# create objects and variables from json file
with open("nodes.json", "r") as f:
    jsonnodes = json.load(f)

for node in jsonnodes:
    obj = server.nodes.objects.add_object(node["node_id"], node["name"])
    for var in node["variables"]:
        opc_var = obj.add_variable(var["node_id"], var["name"], var["value"])
        opc_var.set_writable(True)

# start server
server.start()

try:
    while True:
        time.sleep(0.01)
        for node in jsonnodes:
            for var in node["variables"]:
                var_node = server.get_node(var["node_id"])
                if var["isRandom"]:
                    value = random.randint(var["range_min"], var["range_max"])
                    var_node.set_value(value)
                if "DateTime" in var["name"]:
                    var_node.set_value(datetime.datetime.now())


finally:
    server.stop()



