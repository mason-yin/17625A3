import grpc
from client.inventory_client import Client
import service.A3_pb2 as pb2
import service.A3_pb2_grpc as pb2_grpc


class GetBook:
    def get_book_titles(self, client, isbn_list):
        server_stub = client.inventory_stub()
        res = []
        for i in range(len(isbn_list)):
            isbn = isbn_list[i]
            request = pb2.GetBookByISBNRequest(ISBN=isbn)
            response = server_stub.GetBookByISBN(request)
            res.append(response.book.title)
        return res


if __name__ == '__main__':
    # start the server in server.py!!!
    client = Client('localhost', 50051)
    get_book = GetBook()
    isbn_list = ["9789775325822", "9780155658110"]
    res = get_book.get_book_titles(client, isbn_list)
    for i in range(len(res)):
        print(res[i])
