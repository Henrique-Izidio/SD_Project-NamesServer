import grpc
import time
from grpc_services.server import server_to_server_pb2
from grpc_services.server import server_to_server_pb2_grpc

def run_fake_server(server_id, port, service_name):
    # 1. Conecta ao Servidor de Nomes (ajuste o IP/Porta se necessário)
    channel = grpc.insecure_channel('localhost:50051')
    stub = server_to_server_pb2_grpc.RegistryServiceStub(channel)

    print(f"--- Iniciando Fake Server ID: {server_id} ---")

    try:
        # 2. DISCOVERY: O primeiro registro ("Aluguel")
        record_request = server_to_server_pb2.RecordRequest(
            serverId=server_id,
            serverIp="127.0.0.1",
            serverPort=port,
            overloaded=False,
            service=service_name
        )
        
        response = stub.discovery(record_request)
        
        if response.success:
            print(f"[*] Registro inicial realizado com sucesso para o serviço: {service_name}")
        else:
            print("[!] Falha no registro inicial.")
            return

        # 3. LOOP DE HEARTBEAT: A "Renovação" (Realugar)
        while True:
            time.sleep(30) # Envia a cada 30 segundos
            
            renew_request = server_to_server_pb2.RenewRequest(
                serverId=server_id,
                overloaded=False # Simulando que não está sobrecarregado
            )
            
            print(f"[>] Enviando Heartbeat para ID {server_id}...")
            renew_response = stub.heartBeat(renew_request)
            
            if renew_response.success:
                print(f"    [OK] Lease renovada com sucesso.")
            else:
                print(f"    [ERRO] O NamesServer não reconheceu este ID.")

    except grpc.RpcError as e:
        print(f"[CRITICAL] Erro de conexão com o NamesServer: {e.details()}")
    except KeyboardInterrupt:
        print("\n--- Fake Server desligado pelo usuário ---")

if __name__ == "__main__":
    # Você pode rodar várias instâncias mudando esses valores
    run_fake_server(server_id=1, port=8081, service_name="E-commerce-Payment")