import unittest

from textnode import(
    TextNode,
    TextType,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "url1")
        node2 = TextNode("This is a text node", "bold", "url1")
        self.assertEqual(node, node2)
    
    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(new_nodes)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
        # Test with a single image
        text = "This is an image ![alt text](image.jpg)"
        expected = [("alt text", "image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with multiple images
        text = "Here is one ![first](first.jpg) and another ![second](second.png)"
        expected = [("first", "first.jpg"), ("second", "second.png")]
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with no images
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with images with spaces
        text = "Image with space ![alt text](image file.jpg)"
        expected = [("alt text", "image file.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with images in a paragraph
        text = "Start ![first](first.jpg) middle ![second](second.png) end."
        expected = [("first", "first.jpg"), ("second", "second.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        # Test with a single link
        text = "This is a link [link text](http://example.com)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with multiple links
        text = "Here is one [first](http://first.com) and another [second](http://second.com)"
        expected = [("first", "http://first.com"), ("second", "http://second.com")]
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with no links
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with links with spaces
        text = "Link with space [link text](http://example.com/some page)"
        expected = [("link text", "http://example.com/some page")]
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with links in a paragraph
        text = "Start [first](http://first.com) middle [second](http://second.com) end."
        expected = [("first", "http://first.com"), ("second", "http://second.com")]
        self.assertEqual(extract_markdown_links(text), expected)

class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_images(self):
        # Test with a single image
        old_nodes = [TextNode("This is an image ![alt text](image.jpg)", TextType.TEXT)]
        expected = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "image.jpg"),
        ]
        self.assertEqual(split_nodes_images(old_nodes), expected)

        # Test with multiple images
        old_nodes = [TextNode("First ![first](first.jpg) second ![second](second.png)", TextType.TEXT)]
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "first.jpg"),
            TextNode(" second ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "second.png"),
        ]
        self.assertEqual(split_nodes_images(old_nodes), expected)

        # Test with no images
        old_nodes = [TextNode("This text has no images.", TextType.TEXT)]
        expected = [TextNode("This text has no images.", TextType.TEXT)]
        self.assertEqual(split_nodes_images(old_nodes), expected)

    def test_split_nodes_links(self):
        # Test with a single link
        old_nodes = [TextNode("This is a link [link text](http://example.com)", TextType.TEXT)]
        expected = [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "http://example.com"),
        ]
        self.assertEqual(split_nodes_links(old_nodes), expected)

        # Test with multiple links
        old_nodes = [TextNode("First [first](http://first.com) second [second](http://second.com)", TextType.TEXT)]
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("first", TextType.LINK, "http://first.com"),
            TextNode(" second ", TextType.TEXT),
            TextNode("second", TextType.LINK, "http://second.com"),
        ]
        self.assertEqual(split_nodes_links(old_nodes), expected)

        # Test with no links
        old_nodes = [TextNode("This text has no links.", TextType.TEXT)]
        expected = [TextNode("This text has no links.", TextType.TEXT)]
        self.assertEqual(split_nodes_links(old_nodes), expected)

class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        text = '''This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)'''
        actual_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(actual_nodes, expected)

if __name__ == "__main__":
    unittest.main()