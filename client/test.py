from unittest.mock import MagicMock
from unittest import TestCase, mock

from client.get_book_titles import GetBook
from client.inventory_client import Client

mock_client = MagicMock()
get_book = GetBook()


def my_side_effect(*args):
    dic = {"9780155658110": "Nineteen Eighty-Four", "9780582060104": "Animal Farm",
           "9780395647400": "The Lord of Rings", "9789775325822": "Ozymandias"}
    res = []
    isbn_list = args[1]
    for i in range(len(isbn_list)):
        res.append(dic[isbn_list[i]])
    return res


class TestGetTitles(TestCase):

    def test_mock(self):
        isbn_list = ["9780155658110", "9780395647400"]
        with mock.patch.object(GetBook, 'get_book_titles', side_effect=my_side_effect):
            res = get_book.get_book_titles(mock_client, isbn_list)
            desired = ["Nineteen Eighty-Four", "The Lord of Rings"]
            self.assertIsNotNone(res)
            self.assertListEqual(res, desired)

    def test_live(self):
        # go to server.py to start the server before running this test
        client = Client('localhost', 50051)
        isbn_list = ["9789775325822", "9780155658110"]
        res = get_book.get_book_titles(client, isbn_list)
        desired = ["Ozymandias", "Nineteen Eighty-Four"]
        self.assertIsNotNone(res)
        self.assertListEqual(res, desired)
