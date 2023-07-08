import unittest

from mini_readability.target_extractors import extract


class MyTestCase(unittest.TestCase):
    def test_lenta_ru_parser(self):
        articles = parse()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
