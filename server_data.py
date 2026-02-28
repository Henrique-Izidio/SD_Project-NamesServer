import time

class ServerData:
    serverId: int
    serverIp: str
    serverPort: int
    overloaded: bool
    service: str
    lease: float

    def __init__(self, id, ip, port, isOverloaded, serverService) -> None:
        self.serverId = id
        self.serverIp = ip
        self.serverPort = port
        self.overloaded = isOverloaded
        self.service = serverService
        self.lease = time.time() + 60
    
    def renewLease(self, isOverloaded: bool) -> None:
        self.lease = time.time() + 60
        self.overloaded = isOverloaded
