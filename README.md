## Service Registry & Discovery - Sistema de Bazar

Este repositório contém a implementação do **Servidor de Nomes** para o projeto final da disciplina de **Sistemas Distribuídos**.

O objetivo deste serviço é atuar como um *Service Registry*, permitindo que os servidores de dados se registrem dinamicamente e que os clientes descubram os endereços (IP/Porta) disponíveis para comunicação via gRPC.

## 🛠️ Tecnologias

* **Python 3+**
* **gRPC** (Comunicação entre serviços)
* **Protocol Buffers** (Serialização de dados)
* **Threading** (Controle de concorrência e limpeza de tabela)

## 📋 Funcionalidades

* **Registro Dinâmico:** Servidores de dados anunciam sua presença.
* **Heartbeat (Lease):** Monitoramento de saúde dos servidores registrados.
* **Discovery Service:** Interface dedicada para clientes buscarem serviços ativos.
* **Auto-Cleanup (Reaper):** Remoção automática de servidores que pararem de enviar sinais de vida por mais de 60 segundos.

---

## Como Usar

Siga estes passos para configurar o ambiente e compilar os protocolos.

### 1. Criar o Ambiente Virtual (venv)

Para manter as bibliotecas isoladas e evitar conflitos no seu computador:

```powershell
# Cria a pasta do ambiente virtual
python -m venv venv

# Ativa o ambiente (Windows)
.\venv\Scripts\activate

# Instala as dependências necessárias
 python -m pip install grpcio grpcio-tools

```

### 2. Compilar os Arquivos .proto

Sempre que houver alteração nos arquivos dentro da pasta `/protos`, você precisa gerar o código Python correspondente.

**Certifique-se de que as pastas `grpc_services/server` e `grpc_services/client` existam antes de rodar.**

```powershell
# Compilar protocolo Servidor <-> Servidor (Registry)
python -m grpc_tools.protoc -I./protos --python_out=./grpc_services/server --grpc_python_out=./grpc_services/server ./protos/server_to_server.proto

# Compilar protocolo Servidor <-> Cliente (Discovery)
python -m grpc_tools.protoc -I./protos --python_out=./grpc_services/client --grpc_python_out=./grpc_services/client ./protos/server_to_client.proto

```
**ATENÇÂO:** Qualquer mudanças nos arquivos .proto deve ser repassada para todas as outras partes do projeto, por isso evite alterar eles.

### 3. Rodar o Servidor

Com o ambiente ativo e os protocolos compilados:

```powershell
python names_server.py

```

---

## Estrutura de Pastas

* `/protos`: Contém os contratos `.proto` originais.
* `/grpc_services`: Contém o código Python gerado pelo compilador gRPC.
* `names_server.py`: Código principal com a lógica da tabela de nomes e do servidor.
