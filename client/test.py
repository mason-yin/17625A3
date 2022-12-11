from unittest.mock import patch, Mock
from unittest import TestCase

from client.get_book_titles import getbook
from client.inventory_client import Client
from service.server import start


class TestGetTitles(TestCase):
    @patch('inventory_client.Client')
    def test_mock(self, mock_client):
        client = mock_client()

    def test_live(self):
        client = Client('localhost', 50051)
        isbn_list = ["9789775325822", "9780155658110"]
        res = getbook(client, isbn_list)
        answer = ["Ozymandias", "Nineteen Eighty-Four"]
        self.assertIsNotNone(res)
        self.assertListEqual(res, answer)
