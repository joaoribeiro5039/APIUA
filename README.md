## Introduction
This project provides a monitoring solution for OPC UA servers. It consists of a docker-compose file that sets up multiple OPC UA servers, a Cassandra database, and a Python-based API. The API allows users to set up monitoring activity for a specific node or structure of an OPC UA server.

## Prerequisites
The following prerequisites are required to run the project:
- Docker
- Docker-compose
- Python 3.x
- pip

## Installation
1. Update the package list: 
   ```
   sudo apt update
   ```
2. Install Python3:
   ```
   sudo apt install python3
   ```
3. Install pip:
   ```
   sudo apt install python3-pip
   ```
4. Upgrade pip:
   ```
   pip install --upgrade pip
   ```
5. Install required Python packages for the API:
   ```
   pip install "uvicorn[standard]"
   pip install "fastapi[all]"
   ```
6. Install the Python OPC UA server package:
   ```
   pip install opcua
   ```

## Usage
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd <project-directory>
   ```
3. Run the project:
   ```
   docker-compose up
   ```
4. To run the Python API, open a new terminal window and navigate to the project directory, then run:
   ```
   uvicorn api:app
   ```
5. Use the API endpoints to set up monitoring activity for a specific node or structure of an OPC UA server.

## API Documentation
## OPC UA API Documentation

This API provides endpoints to interact with OPC UA server by reading, writing, and monitoring the values of nodes in the server. 

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Testing
This endpoint returns a Hello World message for testing purposes.

```
GET /Testing
```

#### Read All Values of the OPC UA Server
This endpoint returns all the node values of the OPC UA server.
##### Request
- `opcUrl`: The URL of the OPC UA server. (required)
- `UserName`: The username for authentication. (optional)
- `Password`: The password for authentication. (optional)
- `Secure_Policy`: The secure policy to use. (optional)
##### Response
- A dictionary containing all the node values of the OPC UA server.

```
GET /ReadAllOPCValues?opcUrl=<opcUrl>&UserName=<UserName>&Password=<Password>&Secure_Policy=<Secure_Policy>
```

#### Read Filtered Values of the OPC UA Server
This endpoint returns the node values of the OPC UA server that match a certain node id.
##### Request
- `opcUrl`: The URL of the OPC UA server. (required)
- `nodeid`: The node id to filter by. (required)
- `UserName`: The username for authentication. (optional)
- `Password`: The password for authentication. (optional)
- `Secure_Policy`: The secure policy to use. (optional)
##### Response
- A dictionary containing the node values that match the provided node id.

```
GET /ReadFilteredOPCUAValues?opcUrl=<opcUrl>&nodeid=<nodeid>&UserName=<UserName>&Password=<Password>&Secure_Policy=<Secure_Policy>
```

#### Write Values of the OPC UA Server
This endpoint writes a value to a specific node in the OPC UA server.
##### Request
- `opcUrl`: The URL of the OPC UA server. (required)
- `nodeid`: The node id to write the value to. (required)
- `value`: The value to write. (required)
- `UserName`: The username for authentication. (optional)
- `Password`: The password for authentication. (optional)
- `Secure_Policy`: The secure policy to use. (optional)
##### Response
- A boolean value indicating whether the write was successful.

```
PUT /WriteOPCUAValues?opcUrl=<opcUrl>&nodeid=<nodeid>&value=<value>&UserName=<UserName>&Password=<Password>&Secure_Policy=<Secure_Policy>
```

#### Start Monitoring Activity
This endpoint starts monitoring a specific node in the OPC UA server at a specified frequency.
##### Request
- `Freq`: The frequency of monitoring in seconds. (required)
- `opcUrl`: The URL of the OPC UA server. (required)
- `nodeid`: The node id to monitor. (required)
- `UserName`: The username for authentication. (optional)
- `Password`: The password for authentication. (optional)
- `Secure_Policy`: The secure policy to use. (optional)
##### Response
- A boolean value indicating whether the monitoring was successfully started.

```
POST /StartMonitor?Freq=<Freq>&opcUrl=<opcUrl>&nodeid=<nodeid>&UserName=<UserName>&Password=<Password>&Secure_Policy=<Secure_Policy>
```

#### Stop All Monitoring Activity
This endpoint stops all currently running monitoring tasks.
```
POST /StopMonitor
```

#### Read Monitoring Activity
This endpoint retrieves the data collected from a specific monitoring task.
##### Request
- `opcUrl`: The URL of the OPC UA server. (required)
- `nodeid`: The node id being
## Conclusion
This project provides a simple and efficient monitoring solution for OPC UA servers. By using Docker and Python, it is easy to deploy and use in any environment. With the provided API endpoints, users can easily set up and manage monitoring activities for specific nodes or structures of an OPC UA server.