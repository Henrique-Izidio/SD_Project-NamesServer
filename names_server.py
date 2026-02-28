import time
import grpc
import threading
from concurrent import futures

from grpc_services.client import server_to_client_pb2
from grpc_services.client import server_to_client_pb2_grpc

from grpc_services.server import server_to_server_pb2
from grpc_services.server import server_to_server_pb2_grpc

from server_data import ServerData

class NamesServer(
    server_to_server_pb2_grpc.RegistryServiceServicer,
    server_to_client_pb2_grpc.DiscoveryServiceServicer
): 
    def __init__(self):
        self.name_table = {}
        self.lock = threading.Lock()

        reaper = threading.Thread(target=self.serverReaper, daemon=True)
        reaper.start()
    
    def discovery(self, request, context):
        try:
            if not request.serverIp or request.serverPort <= 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                print(f"Falha ao adicionar Servidor: IP ou Porta invalidos")
                context.set_details("IP ou Porta invalidos")
                return server_to_server_pb2.QueryReply(success = False)

            newServer = ServerData (
                request.serverId,
                request.serverIp,
                request.serverPort,
                request.overloaded,
                request.service,
            )

            with self.lock:
                self.name_table[request.serverId] = newServer

            print(f"Servidor Nº{request.serverId} foi adicionado com sucesso")
            return server_to_server_pb2.QueryReply(success = True)
        except Exception as e:
            print(f"Erro ao registrar servidor: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro interno no servidor de nomes: {str(e)}")
            return server_to_server_pb2.QueryReply(success = False)
     
    def heartBeat(self, request, context):
        try:
            with self.lock:
                if not self.name_table[request.serverId]:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    print(f"Falha ao renovar status. Cria uma nova entrada na rede.")
                    context.set_details("Server already released")
                    return server_to_server_pb2.QueryReply(success = False)
                self.name_table[request.serverId].renewLease(request.overloaded)
                print(f"Servidor {request.serverId} renovado com sucesso")
                return server_to_server_pb2.QueryReply(success = True)
            
        except Exception as e:
            print(f"Erro ao renovar servidor: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro interno no servidor de nomes: {str(e)}")
            return server_to_server_pb2.QueryReply(success = False)
    
    def serverReaper(self):
        print("Inicializando Thread de limpeza...")
        while True:
            time.sleep(10)

            limit = time.time()
            expired_servers = []
            count = 0
            with self.lock:
                for id, data in self.name_table.items():
                    if data.lease <= limit:
                        print(f"Servidor Nº{id} removido por inatividade")
                        expired_servers.append(id)

                for id in expired_servers:
                    del self.name_table[id]
                    count += 1
            
            print(f"{count} servidores removidos")

    def findServer(self, request, context):
        return super().findServer(request, context)

    def warnServerError(self, request, context):
        return super().warnServerError(request, context)
    
def server_start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))

    server_singleton = NamesServer()

    server_to_client_pb2_grpc.add_DiscoveryServiceServicer_to_server(server_singleton, server)
    server_to_server_pb2_grpc.add_RegistryServiceServicer_to_server(server_singleton, server)

    server.add_insecure_port("[::]:50051")

    print("Inicializando Servidor de Nomes...")
    server.start()

    server.wait_for_termination()

if __name__ == "__main__":
    server_start()