import time
from opcua import ua, Server
import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379)

# Create an OPC UA server
server = Server()
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")

# Define the OPC UA namespace
uri = "http://example.com"
idx = server.register_namespace(uri)

# Create a new Object node for the Redis data
objects_node = server.get_objects_node()
redis_node = objects_node.add_object(idx, "RedisData")

# Retrieve keys from Redis and create corresponding Variable nodes
keys = redis_client.keys('*')
for key in keys:
    value = redis_client.get(key)
    var_node = redis_node.add_variable(idx, key.decode('utf-8'), value.decode('utf-8'))
    var_node.set_modelling_rule(True)
    var_node.set_writable()

# Add a Variable node for time
time_variable = redis_node.add_variable(idx, "time", 0.0)
time_variable.set_writable()

# Start the OPC UA server
server.start()

try:
    while True:
        # Update the values of Variable nodes from Redis
        # for key in keys:
        #     value = redis_client.get(key)
        #     var_node = redis_node.get_child([key.decode('utf-8')])
        #     var_node.set_value(value.decode('utf-8'))

        # # Update the time variable
        # current_time = time.time()
        # time_variable.set_value(current_time)

        # Sleep for a while before updating again
        time.sleep(1)

finally:
    # Stop the OPC UA server
    server.stop()
