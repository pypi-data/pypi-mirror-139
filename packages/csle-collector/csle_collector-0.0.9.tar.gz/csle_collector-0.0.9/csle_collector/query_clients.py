from typing import List
import time
import grpc
import csle_collector.client_manager_pb2_grpc
import csle_collector.client_manager_pb2


def get_clients(stub: csle_collector.client_manager_pb2_grpc.ClientManagerStub) \
        -> csle_collector.client_manager_pb2.ClientsDTO:
    """
    Queries the server for the client state

    :param stub: the stub to send the remote gRPC to the server
    :return: a clientsDTO describing the state of the clients
    """
    get_clients_dto_msg = csle_collector.client_manager_pb2.GetClientsMsg()
    clients_dto = stub.getClients(get_clients_dto_msg)
    return clients_dto


def stop_clients(stub: csle_collector.client_manager_pb2_grpc.ClientManagerStub):
    """
    Stops the client arrival process

    :param stub: the stub to the gRPC server
    :return: a clientsDTO describing the state of the clients
    """
    stop_clients_msg = csle_collector.client_manager_pb2.StopClientsMsg()
    clients_dto = stub.stopClients(stop_clients_msg)
    return clients_dto


def start_clients(stub: csle_collector.client_manager_pb2_grpc.ClientManagerStub,
                  mu: float, lamb: int, time_step_len_seconds: int, commands: List[str], num_commands: int=2):
    """
    Starts the client arrival process

    :param stub: the stub to the gRPC server
    :param mu: the mu parameter for the Exponential service time
    :param lamb: the lambda parameter for the Poisson process
    :param time_step_len_seconds: the length of a time-step for simulating the arrival process
    :param num:commands: the number of commands that each client will use
    :return: a clientsDTO describing the state of the clients
    """
    start_clients_msg = csle_collector.client_manager_pb2.StartClientsMsg(
        mu=mu, lamb=lamb, time_step_len_seconds=time_step_len_seconds, commands=commands, num_commands=num_commands
    )
    clients_dto = stub.startClients(start_clients_msg)
    return clients_dto


def run(server: str = "localhost", port: int = 50051):
    with grpc.insecure_channel(f'{server}:{port}') as channel:
        print("creating stub")
        stub = csle_collector.client_manager_pb2_grpc.ClientManagerStub(channel)
        print("stub created")

        print("starting clients")
        clients_dto = start_clients(stub=stub, mu=0.1, lamb=10, time_step_len_seconds=1)
        print(f"num clients:{clients_dto.num_clients}")
        time.sleep(5)
        print("query clients")
        clients_dto = get_clients(stub=stub)
        print(f"num clients:{clients_dto.num_clients}")
        time.sleep(2)
        print("stopping clients")
        clients_dto = stop_clients(stub=stub)
        print(f"num clients:{clients_dto.num_clients}")
        time.sleep(10)
        clients_dto = get_clients(stub=stub)
        print(f"num clients:{clients_dto.num_clients}")


if __name__ == '__main__':
    run(server="localhost", port=50051)

