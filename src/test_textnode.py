import unittest

from textnode import(
    TextNode,
    TextType,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
    markdown_to_blocks,
    is_heading,
    is_code_block,
    is_quote_block,
    is_unordered_list,
    is_ordered_list
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        expected_block_a = "This is **bolded** paragraph"
        expected_block_b = """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line"""
        expected_block_c = """* This is a list
* with items"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], expected_block_a)
        self.assertEqual(blocks[1], expected_block_b)
        self.assertEqual(blocks[2], expected_block_c)

    def test_block_to_block_type(self):
        # Define different blocks of Markdown
        test_cases = {
            "Heading 1": "# Heading 1",
            "Heading 2": "## Heading 2",
            "Code block": "```\nCode block\n```",
            "Quote block": "> Quote block\n> with multiple lines",
            "Unordered list": "* Item 1\n* Item 2",
            "Ordered list": "1. Item 1\n2. Item 2",
            "Paragraph": "This is a normal paragraph.",
            "Mixed content": "# Heading\n\nThis is a paragraph.\n\n```\nCode block\n```"
        }

        # Expected results
        expected_results = {
            "Heading 1": "Heading: # Heading 1",
            "Heading 2": "Heading: ## Heading 2",
            "Code block": "Code block: ```\nCode block\n```",
            "Quote block": "Quote block: > Quote block\n> with multiple lines",
            "Unordered list": "Unordered list: * Item 1\n* Item 2",
            "Ordered list": "Ordered list: 1. Item 1\n2. Item 2",
            "Paragraph": "Paragraph: This is a normal paragraph.",
            "Mixed content": "Heading: # Heading\n\nParagraph: This is a paragraph.\n\nCode block: ```\nCode block\n```"
        }
        
        for name, markdown in test_cases.items():
            with self.subTest(name=name):
                blocks = markdown.split('\n\n')
                result = []
                for block in blocks:
                    block = block.strip()
                    if is_heading(block):
                        result.append(f"Heading: {block}")
                    elif is_code_block(block):
                        result.append(f"Code block: {block}")
                    elif is_quote_block(block):
                        result.append(f"Quote block: {block}")
                    elif is_unordered_list(block):
                        result.append(f"Unordered list: {block}")
                    elif is_ordered_list(block):
                        result.append(f"Ordered list: {block}")
                    else:
                        result.append(f"Paragraph: {block}")
                
                self.assertEqual('\n\n'.join(result), expected_results[name])

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