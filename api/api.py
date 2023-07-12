from fastapi import FastAPI
import asyncio
import datetime
from opcua import ua, Server
from typing import Optional
import redis
import os

global REDIS_HOST
REDIS_HOST = os.getenv("REDIS_HOST")
if REDIS_HOST is None:
    REDIS_HOST = "localhost"


global redis_db
redis_db = redis.Redis(host=REDIS_HOST, port=6379, db=0)


global OPC_Server_Config

global UA_server
UA_server = Server()
# Write data to Redis
redis_db.set('mykey1', 'myvalue1')
redis_db.set('mykey2', 'myvalue2')
redis_db.set('mykey3', 'myvalue3')

tyest = redis_db.get('*')

# Read data from Redis
value = redis_db.get('mykey')

def UpdateOPCStructure():
    global UA_server, OPC_Server_Config, redis_db
    a = 1
    
    UA_server.start()

def SetOPCServer(ip:str,name:str, uri:str):
    global OPC_Server_Config, UA_server
    UA_server.stop()
    obj ={
        "IP": ip,
        "Name": name,
        "URI": uri
    }
    UA_server = Server()
    UA_server.set_endpoint("opc.tcp://" + obj["IP"] + ":4840/" +obj["Name"])
    UpdateOPCStructure()
    UA_server.start()
    OPC_Server_Config = obj
    return True

# def AddNode(obj_id:str, obj_name:str):

app = FastAPI()

#Testing
@app.get("/Testing")
async def root():
    return {"message": "Hello World"}

#Add new OPC Object
@app.put("/SetOPCServer")
async def root(ip:str,name:str, uri:str):
    return SetOPCServer(ip,name,uri)

#Add new OPC Object
@app.put("/AddObject")
async def root(obj_id:str, obj_name:str):
    return AddObject(obj_id,obj_name)

#Add new OPC Node
@app.put("/AddNode")
async def root(obj_id:str, obj_name:str):
    return {"message": "Hello World"}

#On Shutdown
@app.on_event("shutdown")
async def shutdown_event():
    print("Stopping pending Tasks")
    await asyncio.sleep(1)
    print("Shutting down...")