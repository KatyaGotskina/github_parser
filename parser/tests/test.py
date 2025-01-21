import unittest
import requests
from starlette import status


class TestGetTop100(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://localhost:8001/api/repos"
        self.client = requests.Session()

    def test_get_top100_success(self):
        response = self.client.get(f"{self.base_url}/top100")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == '__main__':
    unittest.main()
