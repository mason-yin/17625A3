import grpc
from client.inventory_client import Client
import service.A3_pb2 as pb2
import service.A3_pb2_grpc as pb2_grpc


def getbook(client, isbn_list):
    server_stub = client.inventory_stub()
    res = []
    for i in range(len(isbn_list)):
        isbn = isbn_list[i]
        request = pb2.GetBookByISBNRequest(ISBN=isbn)
        response = server_stub.GetBookByISBN(request)
        res.append(response.book.title)
    return res


if __name__ == '__main__':
    client = Client('localhost', 50051)
    isbn_list = ["9789775325822", "9780155658110"]
    res = getbook(client, isbn_list)
    for i in range(len(res)):
        print(res[i])
