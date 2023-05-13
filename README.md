# OPCUAWatchdog
Solution for Data Sincronization between Several OPC UA Servers

## Requirements

sudo apt update
sudo apt install python3
sudo apt install python3-pip

# Python API
pip install --upgrade pip
pip install "uvicorn[standard]"
pip install "fastapi[all]"

# Python OPC UA Server
pip install --upgrade pip
pip install opcua


# Run Python API
uvicorn api:app
