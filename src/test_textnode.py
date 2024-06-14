import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "url1")
        node2 = TextNode("This is a text node", "bold", "url1")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()