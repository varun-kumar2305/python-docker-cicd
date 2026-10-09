import unittest
from http.client import HTTPConnection
from threading import Thread
from http.server import HTTPServer

from app import Handler


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_homepage_response(self):
        connection = HTTPConnection("127.0.0.1", self.port)
        connection.request("GET", "/")
        response = connection.getresponse()

        self.assertEqual(response.status, 200)
        self.assertEqual(
            response.read(),
            b"Hello from Docker Python App!"
        )
        connection.close()


if __name__ == "__main__":
    unittest.main()
