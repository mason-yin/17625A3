from concurrent import futures
import grpc
import time
import logging
import service.A3_pb2 as pb2
import service.A3_pb2_grpc as pb2_grpc


class HelloWorldService(pb2_grpc.HelloWorldServicer):

    def __init__(self, *args, **kwargs):
        pass

    def HelloWorld(self, request, context):
        return pb2.HelloWorldResponse(response="Hello World!")


class InventoryService(pb2_grpc.InventoryServiceServicer):

    def __init__(self, *args, **kwargs):
        # hardcode book details
        book1 = {"ISBN": "9780155658110",
                 "title": "Nineteen Eighty-Four",
                 "author": "George Orwell",
                 "genre": 0,
                 "publish_year": 1949}
        book2 = {"ISBN": "9780582060104",
                 "title": "Animal Farm",
                 "author": "George Orwell",
                 "genre": 1,
                 "publish_year": 1945}
        book3 = {"ISBN": "9780395647400",
                 "title": "The Lord of Rings",
                 "author": "J. R. R. Tolkien",
                 "genre": 2,
                 "publish_year": 1954}
        book4 = {"ISBN": "9789775325822",
                 "title": "Ozymandias",
                 "author": "Percy Bysshe Shelley",
                 "genre": 3,
                 "publish_year": 1818}
        self.books = {"9780155658110": book1,
                      "9780582060104": book2,
                      "9780395647400": book3,
                      "9789775325822": book4}

    def GetBookByISBN(self, request, context):
        if request.ISBN is None:
            # ISBN field does not exist
            print("here")
        isbn = request.ISBN
        if isbn not in self.books:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("The book does not exist")
            return pb2.GetBookByISBNResponse()
        response = self.books[isbn]
        return pb2.GetBookByISBNResponse(book=response)

    def CreateBook(self, request, context):
        if request.book.ISBN in self.books:
            # book already exists
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("The book already exists")
            return pb2.CreateBookResponse()
        book = {"ISBN": request.book.ISBN,
                "title": request.book.title,
                "author": request.book.author,
                "genre": request.book.genre,
                "publish_year": request.book.publish_year}

        self.books[request.book.ISBN] = book
        return pb2.CreateBookResponse(response="Create Success")


def start():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_HelloWorldServicer_to_server(HelloWorldService(), server)
    pb2_grpc.add_InventoryServiceServicer_to_server(InventoryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    start()
