from fastapi import FastAPI
import asyncio
import datetime
from opcua import Client, ua
from typing import Optional
from cassandra.cluster import Cluster

global cluster
global session 

cluster = Cluster(["cassandra"])
session = cluster.connect()

def StoreTolocalCassandra(table: str, data: str):
    time = str(datetime.datetime.now())
    global session
    query = f"INSERT INTO {table.lower()} (id, data) VALUES (%s, %s)"
    session.execute(query, (time, data))

def RetrieveDataFromCassandra(table: str):
    global session
    
    session.set_keyspace('opcmonitor')
    rows = session.execute('SELECT * FROM monitorids')
    DataKey = "empty"
    for row in rows:
        if row.runningmonitor == table:
            DataKey = row.id
            break
    if DataKey == "empty":
        return False
    return session.execute(str("SELECT * FROM " + DataKey.lower()))


RetrieveDataFromCassandra("opc.tcp://localhost:4840ns=1")

security_policies = {
    "NoSecurity": ua.SecurityPolicyType.NoSecurity,
    "Basic128Rsa15_Sign": ua.SecurityPolicyType.Basic128Rsa15_Sign,
    "Basic128Rsa15_SignAndEncrypt": ua.SecurityPolicyType.Basic128Rsa15_SignAndEncrypt,
    "Basic256_Sign": ua.SecurityPolicyType.Basic256_Sign,
    "Basic256_SignAndEncrypt": ua.SecurityPolicyType.Basic256_SignAndEncrypt,
    "Basic256Sha256_Sign": ua.SecurityPolicyType.Basic256Sha256_Sign,
    "Basic256Sha256_SignAndEncrypt": ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt
}

def ReadAllOPCUAValues(opcUrl : str, UserName : Optional[str] = None, Password : Optional[str] = None , Secure_Policy : Optional[str] = None):
    if (UserName is None) and (Password is None) and (Secure_Policy is None) :
        client = Client(opcUrl)
    else:
        security_policy = security_policies[Secure_Policy]
        user_token_policy = ua.UserTokenPolicy()
        user_token_policy.set_userpass(UserName, Password)
        security_settings = ua.SecuritySettings()
        security_settings.set_security_policy(security_policy)
        security_settings.set_user_token_policy(user_token_policy)
        client.set_security_string(security_settings)
        client = Client(opcUrl)

    client.connect()
    CurrentNodeValues = {}
    root = client.get_root_node()
    objects = root.get_children()[0]
    nodes = objects.get_children()
    for node in nodes:
        for subnode in node.get_children():
            if "ns=1" in str(subnode):
                node_id = str(subnode)
                value = client.get_node(node_id).get_value()
                CurrentNodeValues.update({node_id:value})
    
    client.disconnect()
    return CurrentNodeValues

def WriteOPCUAValues(opcUrl : str, nodeid : str, value : str, UserName : Optional[str] = None, Password : Optional[str] = None , Secure_Policy : Optional[str] = None):
    if (UserName is None) and (Password is None) and (Secure_Policy is None) :
        client = Client(opcUrl)
    else:
        security_policy = security_policies[Secure_Policy]
        user_token_policy = ua.UserTokenPolicy()
        user_token_policy.set_userpass(UserName, Password)
        security_settings = ua.SecuritySettings()
        security_settings.set_security_policy(security_policy)
        security_settings.set_user_token_policy(user_token_policy)
        client.set_security_string(security_settings)
        client = Client(opcUrl)
    client.connect()
    client.get_node(nodeid).set_value(value)
    client.disconnect()

async def Monitor(Freq : int, opcUrl : str, nodeid : str, UserName :  Optional[str] = None, Password :  Optional[str] = None , Secure_Policy :  Optional[str] = None): 
    global StopFlag
    global session
    monitorID = str(opcUrl+nodeid)
    session.execute("CREATE KEYSPACE IF NOT EXISTS opcmonitor WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}")
    session.set_keyspace('opcmonitor')
    session.execute("CREATE TABLE IF NOT EXISTS monitorids (id text PRIMARY KEY, RunningMonitor text)")
    rows = session.execute('SELECT * FROM monitorids')
    DataKey = "empty"
    for row in rows:
        if row.runningmonitor == monitorID:
            DataKey = row.id
            break
    if DataKey == "empty":
        DataKey = str('MonitorData' + '0')
        query = f"INSERT INTO monitorids (id, RunningMonitor) VALUES (%s, %s)"
        session.execute(query, (DataKey, monitorID))

    session.execute(str("CREATE TABLE IF NOT EXISTS " + DataKey + " (id text PRIMARY KEY, data text)"))

    if (UserName is None) and (Password is None) and (Secure_Policy is None) :
        client = Client(opcUrl)
    else:
        security_policy = security_policies[Secure_Policy]
        user_token_policy = ua.UserTokenPolicy()
        user_token_policy.set_userpass(UserName, Password)
        security_settings = ua.SecuritySettings()
        security_settings.set_security_policy(security_policy)
        security_settings.set_user_token_policy(user_token_policy)
        client.set_security_string(security_settings)
        client = Client(opcUrl)

    client.connect()
    while not StopFlag:
        CurrentNodeValues = {}
        root = client.get_root_node()
        objects = root.get_children()[0]
        nodes = objects.get_children()
        for node in nodes:
            for subnode in node.get_children():
                if "ns=1" in str(subnode):
                    node_id = str(subnode)
                    value = client.get_node(node_id).get_value()
                    CurrentNodeValues.update({node_id:value})
        MonitorCollection = {node_id: Current_value for node_id, Current_value in CurrentNodeValues.items() if nodeid in node_id}
        json_string = str(MonitorCollection)
        StoreTolocalCassandra(DataKey,json_string)
        await asyncio.sleep(1/Freq)

    client.disconnect()

app = FastAPI()


#Testing
@app.get("/Testing")
async def root():
    return {"message": "Hello World"}

# Get all Values of the OPC UA Server
@app.get("/ReadAllOPCValues")
def opcuavalues(opcUrl : str, UserName : Optional[str] = None, Password : Optional[str] = None , Secure_Policy : Optional[str] = None):
    return ReadAllOPCUAValues(opcUrl, UserName, Password, Secure_Policy)

# Get Filtered Values of the OPC UA Server
@app.get("/ReadFilteredOPCUAValues")
def opcuavalues(opcUrl : str, nodeid : str, UserName :  Optional[str] = None, Password :  Optional[str] = None , Secure_Policy :  Optional[str] = None):
    NodeColletion = ReadAllOPCUAValues(opcUrl, UserName, Password, Secure_Policy)
    return {node_id: Current_value for node_id, Current_value in NodeColletion.items() if nodeid in node_id}

# Get Filtered Values of the OPC UA Server
@app.put("/WriteOPCUAValues")
def opcuavalues(opcUrl : str, nodeid : str, value : str, UserName :  Optional[str] = None, Password :  Optional[str] = None , Secure_Policy :  Optional[str] = None):
    WriteOPCUAValues(opcUrl, nodeid, value, UserName, Password, Secure_Policy)
    return {True}

#Start Monitoring Activity
@app.post("/StartMonitor")
async def Start_Monitor(Freq : int, opcUrl : str, nodeid : str, UserName :  Optional[str] = None, Password :  Optional[str] = None , Secure_Policy :  Optional[str] = None):
    global RunningTasks
    global StopFlag
    StopFlag = False
    RunningTasks = asyncio.create_task(Monitor(Freq, opcUrl, nodeid, UserName, Password, Secure_Policy))
    return True

# Get Filtered Values of the OPC UA Server
@app.get("/ReadFilteredOPCUAValues")
def opcuavalues(opcUrl : str, nodeid : str, UserName :  Optional[str] = None, Password :  Optional[str] = None , Secure_Policy :  Optional[str] = None):
    NodeColletion = ReadAllOPCUAValues(opcUrl, UserName, Password, Secure_Policy)
    return {node_id: Current_value for node_id, Current_value in NodeColletion.items() if nodeid in node_id}

#Stop All Monitoring Activity
@app.post("/StopMonitor")
async def Start_Monitor():
    global StopFlag
    StopFlag = True
    return True

#Read All Monitoring Activity
@app.get("/ReadMonitor")
async def Read_Monitor(opcUrl : str, nodeid : str):
    monitorID = str(opcUrl+nodeid)
    return RetrieveDataFromCassandra(monitorID)

#On Shutdown
@app.on_event("shutdown")
async def shutdown_event():
    global StopFlag
    StopFlag = True
    print("Stopping pending Tasks")
    await asyncio.sleep(1)
    session.shutdown()
    cluster.shutdown()
    print("Shutting down...")