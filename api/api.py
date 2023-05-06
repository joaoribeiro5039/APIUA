from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

#Testing
@app.get("/Testing")
async def root():
    return {"message": "Hello World"}


#CurrentTime
@app.get("/current-time")
def get_current_time():
    current_time = datetime.now()
    return {"Current_Time": str(current_time)}

#CurrentTime
@app.get("/TestConnection")
def get_current_time():
    current_time = datetime.now()
    return {"Current_Time": str(current_time)}
