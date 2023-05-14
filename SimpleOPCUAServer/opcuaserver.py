from opcua import ua, Server
import time
import random
import datetime
import json

opcConfig = [
    {
        "node_id": "ns=1;s=Machine1",
        "name": "Machine1",
        "variables": [
            {
                "node_id": "ns=1;s=Machine1.Speed",
                "name": "Speed",
                "value": 0,
                "isRandom": True,
                "range_min": 200,
                "range_max": 400
            },
            {
                "node_id": "ns=1;s=Machine1.Temperature",
                "name": "Temperature",
                "value": 0,
                "range": 0,
                "isRandom": True,
                "range_min": 300,
                "range_max": 400
            },
            {
                "node_id": "ns=1;s=Machine1.State",
                "name": "State",
                "value": 0,
                "isRandom": False,
                "range_min": 0,
                "range_max": 5
            },
            {
                "node_id": "ns=1;s=Machine1.DateTime",
                "name": "DateTime",
                "value": 0,
                "isRandom": False,
                "range_min": 0,
                "range_max": 0
            }
        ]
    },
    {
        "node_id": "ns=1;s=Machine2",
        "name": "Machine2",
        "variables": [
            {
                "node_id": "ns=1;s=Machine2.Speed",
                "name": "Speed",
                "value": 0,
                "isRandom": True,
                "range_min": 200,
                "range_max": 400
            },
            {
                "node_id": "ns=1;s=Machine2.Temperature",
                "name": "Temperature",
                "value": 0,
                "isRandom": True,
                "range_min": 300,
                "range_max": 400
            },
            {
                "node_id": "ns=1;s=Machine2.State",
                "name": "State",
                "value": 0,
                "isRandom": False,
                "range_min": 0,
                "range_max": 5
            },
            {
                "node_id": "ns=1;s=Machine2.DateTime",
                "name": "DateTime",
                "value": 0,
                "isRandom": False,
                "range_min": 0,
                "range_max": 0
            }
        ]
    }
]

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
        for node in opcConfig:
            for var in node["variables"]:
                var_node = server.get_node(var["node_id"])
                if var["isRandom"]:
                    value = random.randint(var["range_min"], var["range_max"])
                    var_node.set_value(value)
                if "DateTime" in var["name"]:
                    var_node.set_value(datetime.datetime.now())


finally:
    server.stop()



