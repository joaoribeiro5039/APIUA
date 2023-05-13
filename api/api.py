from fastapi import FastAPI
from datetime import datetime
from opcua import Client, ua
from typing import Optional

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


print(ReadAllOPCUAValues("opc.tcp://localhost:4840"))
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
