from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
        # import pdb; pdb.set_trace()
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
            else:
                segments = old_node.text.split(delimiter)
                for i, segment in enumerate(segments):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(segment, old_node.text_type))
                    else:
                        new_nodes.append(TextNode(segment, text_type))
        return new_nodes

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
    raise Exception("Unsupported TextNode type")

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        cond1 = self.text == node.text
        cond2 = self.text_type == node.text_type
        cond3 = self.url == node.url
        return (cond1 and cond2 and cond3)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"