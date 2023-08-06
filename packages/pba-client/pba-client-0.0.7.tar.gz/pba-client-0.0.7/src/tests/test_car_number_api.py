import unittest

from src.pba_client.client import PBAClient


class TestCarNumberAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = PBAClient("", "")

    def test_is_car_number_not_found(self):
        car_number = ""
        result_data = self.api_client.search_car_number(car_number)
        self.assertIn('code', result_data)
        self.assertIn('message', result_data)

        result_code = result_data.get("code")
        self.assertIsInstance(result_code, int)
        self.assertEqual(result_code, 404)

        result_message = result_data.get("message")
        self.assertIsInstance(result_message, str)
        self.assertEqual(result_message, "Invalid car number")


if __name__ == '__main__':
    unittest.main()
