import unittest

from whatdo import app


class EndpointTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertTrue(rv.is_json)
        data = rv.get_json()
        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
