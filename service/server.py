from concurrent import futures
import grpc
import logging
import service.A3_pb2 as pb2
import service.A3_pb2_grpc as pb2_grpc


# a simple helloworld service
class HelloWorldService(pb2_grpc.HelloWorldServicer):

    def __init__(self, *args, **kwargs):
        pass

    def HelloWorld(self, request, context):
        return pb2.HelloWorldResponse(response="Hello World!")


# the Inventory Service
class InventoryService(pb2_grpc.InventoryServiceServicer):

    def __init__(self, *args, **kwargs):
        # hardcode book details when initialized
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

    # controller for getting book detail by ISBN
    def GetBookByISBN(self, request, context):
        if not request.HasField("ISBN"):
            # ISBN field is missing
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("The ISBN field is missing")
            return pb2.GetBookByISBNResponse()
        isbn = request.ISBN
        if isbn not in self.books:
            # book does not exist
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("The book does not exist")
            return pb2.GetBookByISBNResponse()
        response = self.books[isbn]
        return pb2.GetBookByISBNResponse(book=response)

    # controller for creating new book
    def CreateBook(self, request, context):
        all_field_valid = request.book.HasField("ISBN") and request.book.HasField("title") \
                          and request.book.HasField("author") and request.book.HasField("genre") \
                          and request.book.HasField("publish_year")
        if not all_field_valid:
            # Argument fields are not valid
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Request fields are not valid")
            return pb2.CreateBookResponse()
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
        print(len(self.books))
        return pb2.CreateBookResponse(response="Create Success")


# start server
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
