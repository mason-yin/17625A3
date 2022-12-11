import grpc
import service.A3_pb2 as pb2
import service.A3_pb2_grpc as pb2_grpc


class Client(object):
    """
    Client for Assignment4
    """

    def __init__(self, host, port):
        self.host = host
        self.server_port = port

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.HelloWorldStub = pb2_grpc.HelloWorldStub(self.channel)
        self.InventoryServiceStub = pb2_grpc.InventoryServiceStub(self.channel)

    def helloworld(self, message):
        message = pb2.HelloWorldRequest(request=message)
        print(f'{message}')
        return self.HelloWorldStub.HelloWorld(message)

    def inventory_stub(self):
        return self.InventoryServiceStub


if __name__ == '__main__':
    # client class test code
    # do not forget to start the server before running following code
    client = Client('localhost', 50051)
    result = client.helloworld("Hello Server!")
    print(f'{result}')
