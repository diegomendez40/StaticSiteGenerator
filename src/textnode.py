from htmlnode import LeafNode
from enum import Enum
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text != None and old_node.text != "":
            image_tups = extract_markdown_images(old_node.text)
            if image_tups != []:
                text_to_split = old_node.text
                for image_tup in image_tups:
                    segments = text_to_split.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                    new_nodes.append(TextNode(segments[0], old_node.text_type))
                    new_nodes.append(TextNode(image_tup[0], TextType.IMAGE, image_tup[1]))
                    if len(segments) > 1 and segments[1] != "":
                        text_to_split = segments[1]
                if len(segments) > 1 and segments[1] != "":
                    new_nodes.append(TextNode(segments[1], old_node.text_type))
            else:
                new_nodes.append(TextNode(old_node.text, old_node.text_type, old_node.url))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text != None and old_node.text != "":
            link_tups = extract_markdown_links(old_node.text)
            if link_tups != []:
                text_to_split = old_node.text
                for link_tup in link_tups:
                    segments = text_to_split.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                    new_nodes.append(TextNode(segments[0], old_node.text_type))
                    new_nodes.append(TextNode(link_tup[0], TextType.LINK, link_tup[1]))
                    if len(segments) > 1 and segments[1] != "":
                        text_to_split = segments[1]
                if len(segments) > 1 and segments[1] != "":
                    new_nodes.append(TextNode(segments[1], old_node.text_type))
            else:
                new_nodes.append(TextNode(old_node.text, old_node.text_type, old_node.url))
    return new_nodes

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

def textnode_to_html_node(text_node):
    # Eliminamos \n porque equivale a espacio en html
    unbroken_text = text_node.text.replace('\n', ' ')
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, unbroken_text)
        case TextType.BOLD:
            return LeafNode("b", unbroken_text)
        case TextType.ITALIC:
            return LeafNode("i", unbroken_text)
        case TextType.CODE:
            return LeafNode("code", unbroken_text)
        case TextType.LINK:
            return LeafNode("a", unbroken_text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":unbroken_text})
    raise Exception("Unsupported TextNode type")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    # import pdb; pdb.set_trace()
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

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