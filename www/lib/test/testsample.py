import unittest

class TestSample(unittest.TestCase):
    def test_1(self):
        self.assertTrue(True)
        
    def test_2(self):
        self.assertEqual(3, 2+1)