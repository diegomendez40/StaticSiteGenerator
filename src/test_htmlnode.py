import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

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

class TestParentNode(unittest.TestCase):

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node.to_html()
        html = '''<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'''
        self.assertEqual(f"{node.to_html()}", html)

    def test_to_html2(self):
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Text before"),
                ParentNode(
                    "span",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, " inside span"),
                    ],
                ),
                LeafNode(None, "Text after"),
            ],
        )
        html = '''<div>Text before<span><b>Bold text</b> inside span</span>Text after</div>'''
        self.assertEqual(f"{node.to_html()}", html)

    def test_to_html3(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
                ParentNode("li", [LeafNode(None, "Item 3")]),
            ],
        )
        html = '''<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>'''
        self.assertEqual(f"{node.to_html()}", html)

if __name__ == "__main__":
    unittest.main()