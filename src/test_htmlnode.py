import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):

    def test_props(self):
        node = HTMLNode("a", "Este es el texto", props={"href": "https://www.google.com"})
        node2 = HTMLNode("a", "Este es el texto", props={"href": "https://www.google.com"})
        self.assertEqual(f"{node}", f"{node2}")

class TestLeafNode(unittest.TestCase):

    def test_to_html(self):
        node = LeafNode("a", "Este es el texto", props={"href": "https://www.google.com"})
        node2 = LeafNode("a", "Este es el texto", props={"href": "https://www.google.com"})
        self.assertEqual(f"{node.to_html()}", f"{node2.to_html()}")

    def test_to_html2(self):
        node = LeafNode("p", "This is a paragraph of text.")
        html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(f"{node.to_html()}", html)

    def test_to_html3(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html = '''<a href="https://www.google.com">Click me!</a>'''
        self.assertEqual(f"{node.to_html()}", html)


if __name__ == "__main__":
    unittest.main()