from opcua import Client

url = "opc.tcp://localhost:4840"

client = Client(url)
client.connect()

root = client.get_root_node()

objects = root.get_children()[0]

nodes = objects.get_children()
for node in nodes:
    subnodes = node.get_children()
    for subnode in subnodes:
        if "ns=1" in str(subnode):
            node_id = str(subnode)
            value = client.get_node(node_id).get_value()
            print(node_id)
            print(value)
    

client.disconnect()
