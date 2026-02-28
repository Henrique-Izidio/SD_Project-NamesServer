import grpc
import threading
from concurrent import futures

from grpc_services.client import server_to_client_pb2
from grpc_services.client import server_to_client_pb2_grpc

from grpc_services.server import server_to_server_pb2
from grpc_services.server import server_to_server_pb2_grpc

class NamesServer(
    server_to_server_pb2_grpc.RegistryServiceServicer,
    server_to_client_pb2_grpc.DiscoveryServiceServicer
): 
    def __init__(self):
        self.name_table = {}
        self.lock = threading.Lock()
    
    def discovery(self, request, context):
        return super().discovery(request, context)
    
    def heartBeat(self, request, context):
        return super().heartBeat(request, context)
    
    def findServer(self, request, context):
        return super().findServer(request, context)

    def warnServerError(self, request, context):
        return super().warnServerError(request, context)
    
def server_start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))

    server_singleton = NamesServer()

    server_to_client_pb2_grpc.add_DiscoveryServiceServicer_to_server(server_singleton, server)
    server_to_server_pb2_grpc.add_RegistryServiceServicer_to_server(server_singleton, server)

    print("Inicializando Servidor de Nomes...")
    server.start()

    server.wait_for_termination()
if __name__ == "__main__":
    server_start()