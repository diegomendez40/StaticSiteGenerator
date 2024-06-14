import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props(self):
        node = HTMLNode(tag_str="a", value="Este es el texto", props={"href": "https://www.google.com"})
        node2 = HTMLNode(tag_str="a", value="Este es el texto", props={"href": "https://www.google.com"})
        self.assertEqual(f"{node}", f"{node2}")


if __name__ == "__main__":
    unittest.main()