from fastapi import FastAPI
from datetime import datetime
from opcua import Client

url = "opc.tcp://localhost:4840"  # replace with your OPC UA server's URL

client = Client(url)
client.connect()

app = FastAPI()

#Testing
@app.get("/Testing")
async def root():
    return {"message": "Hello World"}

# Define a GET endpoint to retrieve the current client URLs
@app.get("/opcuavalues")
def get_opcua_urls():
    return {"urls": list(clients.keys())}

# Define a SET endpoint to update the client URL for a specific server
@app.set("/opcua-url/")
def set_opcua_url(server_name: str, url: str):
    if server_name in clients:
        clients[server_name].disconnect()
    clients[server_name] = create_client(url)
    return {"message": f"Client URL for {server_name} updated successfully"}

# Define an endpoint to test the connection to a specific server
@app.get("/TestConnection/")
def test_connection(server_name: str):
    if server_name not in clients:
        return {"error": f"Server {server_name} not found"}
    if clients[server_name].uaclient.get_state() == "Connected":
        return {"message": f"Connection to {server_name} successful"}
    else:
        return {"message": f"Connection to {server_name} failed"}



# Define a shutdown event to disconnect all clients when the server is stopped
@app.on_event("shutdown")
def shutdown_event():
    for client in clients.values():
        client.disconnect()