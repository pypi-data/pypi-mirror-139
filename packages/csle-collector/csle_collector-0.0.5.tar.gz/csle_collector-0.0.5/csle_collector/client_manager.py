import threading
import time
from scipy.stats import poisson
from scipy.stats import expon
from concurrent import futures
import grpc
import csle_collector.client_manager_pb2_grpc
import csle_collector.client_manager_pb2


class ClientThread(threading.Thread):
    """
    Thread representing a client
    """

    def __init__(self, service_time: float) -> None:
        """
        Initializes the client

        :param service_time: the service time of the client
        """
        threading.Thread.__init__(self)
        self.service_time = service_time

    def run(self) -> None:
        """
        The main function of the client

        :return: None
        """
        time.sleep(self.service_time)


class ArrivalThread(threading.Thread):
    """
    Thread that generates client arrivals (starts client threads according to a Poisson process)
    """

    def __init__(self, time_step_len_seconds: float, lamb: int = 10, mu: float = 0.1):
        """
        Initializes the arrival thread

        :param time_step_len_seconds: the number of seconds that one time-unit of the Poisson process corresponds to
        :param lamb: the lambda parameter of the Poisson process for arrivals
        :param mu: the mu parameter of the service times of the clients
        """
        threading.Thread.__init__(self)
        self.time_step_len_seconds = time_step_len_seconds
        self.client_threads = []
        self.t = 0
        self.lamb = lamb
        self.mu = mu
        self.stopped = False

    def run(self) -> None:
        """
        Runs the arrival generator, generates new clients dynamically according to a Poisson process

        :return: None
        """
        while not self.stopped:
            new_client_threads = []
            for ct in self.client_threads:
                if ct.is_alive():
                    new_client_threads.append(ct)
            self.client_threads = new_client_threads
            self.t += 1
            new_clients = poisson.rvs(self.lamb*self.time_step_len_seconds, size=1)[0]
            for nc in range(new_clients):
                service_time = expon.rvs(scale=1/(self.mu*(self.time_step_len_seconds)), loc=0, size=1)[0]
                thread = ClientThread(service_time=service_time)
                thread.start()
                self.client_threads.append(thread)
            time.sleep(self.time_step_len_seconds)


class ClientManagerServicer(csle_collector.client_manager_pb2_grpc.ClientManagerServicer):
    """
    gRPC server for managing the running clients. Allows to start/stop clients remotely and also to query the
    state of the clients.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        self.arrival_thread = None

    def getClients(self, request: csle_collector.client_manager_pb2.GetClientsMsg, context: grpc.ServicerContext) \
            -> csle_collector.client_manager_pb2.ClientsDTO:
        """
        Gets the state of the clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        num_clients = 0
        if self.arrival_thread is not None:
            num_clients = len(self.arrival_thread.client_threads)
        clients_dto = csle_collector.client_manager_pb2.ClientsDTO(
            num_clients = num_clients,
            client_process_active = True
        )
        return clients_dto

    def stopClients(self, request: csle_collector.client_manager_pb2.StopClientsMsg, context: grpc.ServicerContext):
        """
        Stops the Poisson-process that generates new clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        print("Stopping clients")
        if self.arrival_thread is not None:
            self.arrival_thread.stopped = True
            time.sleep(1)
        self.arrival_thread = None

        return csle_collector.client_manager_pb2.ClientsDTO(
            num_clients = 0,
            client_process_active = True
        )

    def startClients(self, request: csle_collector.client_manager_pb2.StartClientsMsg,
                     context: grpc.ServicerContext) -> csle_collector.client_manager_pb2.ClientsDTO:
        """
        Starts/Restarts the Poisson process that generates clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        print("Starting clients")
        if self.arrival_thread is not None:
            self.arrival_thread.stopped = True
            time.sleep(1)

        if request.time_step_len_seconds <= 0:
            request.time_step_len_seconds = 1
        arrival_thread = ArrivalThread(time_step_len_seconds=request.time_step_len_seconds,
                                       lamb=request.lamb, mu=request.mu)
        arrival_thread.start()
        self.arrival_thread = arrival_thread

        clients_dto = csle_collector.client_manager_pb2.ClientsDTO(
            num_clients = len(self.arrival_thread.client_threads),
            client_process_active = True
        )
        return clients_dto


def serve(port : int = 50051) -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    csle_collector.client_manager_pb2_grpc.add_ClientManagerServicer_to_server(
        ClientManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"ClientManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve(port=50051)



