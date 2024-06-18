from textnode import (
    text_to_textnodes,
    textnode_to_html_node
)
from enum import Enum
from htmlnode import (
    ParentNode,
)
import re

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered list"

def block_to_block_type(markdown):
    block = markdown.strip()
    if is_heading(block):
        return BlockType.HEAD
    elif is_code_block(block):
        return BlockType.CODE
    elif is_quote_block(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UL
    elif is_ordered_list(block):
        return BlockType.OL
    else:
        return BlockType.PARA

def get_html_tag(block_type):
    match block_type:
        case BlockType.PARA:
            return "p"
        case BlockType.HEAD:
            return "h1"   # Añadir otros encabezamientos
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UL:
            return "ul"
        case BlockType.OL:
            return "ol"

def is_heading(block):
    return bool(re.match(r'^#{1,6} ', block))

def is_code_block(block):
    return block.startswith('```') and block.endswith('```')

def is_quote_block(block):
    return all(line.startswith('>') for line in block.split('\n'))

def is_unordered_list(block):
    return all(re.match(r'^[*-] ', line) for line in block.split('\n'))

def is_ordered_list(block):
    lines = block.split('\n')
    for i, line in enumerate(lines, start=1):
        if not re.match(r'^{idx}\. '.format(idx=i), line):
            return False
    return True

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            stripped_blocks.append(stripped)
    return stripped_blocks

"""This one should make use of a lot of the previous functionality to convert a full markdown document into an HTMLNode.
That top-level HTMLNode should just be a <div>, where each child is a block of the document. Each block should have its own "inline" children.
"""
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children_nodes = [MDBlock(block).to_html_node() for block in blocks]
    html_parent_node = ParentNode("div", html_children_nodes)
    return html_parent_node

def mdstrip(block, block_type):
    match block_type:
        case BlockType.PARA:
            clean_block = block
            return clean_block
        case BlockType.HEAD:
            clean_block = remove_md_heading_hashes(block)
            return clean_block
        case BlockType.CODE:
            clean_block = remove_md_code_prefix(block)
            return clean_block
        case BlockType.QUOTE:
            clean_block = remove_md_quote_prefix(block)
            return clean_block
        case BlockType.UL:
            clean_block = remove_md_unordered_list_prefix(block)
            return clean_block
        case BlockType.OL:
            clean_block = remove_md_ordered_list_prefix(block)
            return clean_block

def remove_md_heading_hashes(heading):
    # Usa una expresión regular para quitar entre 1 y 6 almohadillas al principio del heading
    return re.sub(r'^#{1,6}\s*', '', heading)

def remove_md_code_prefix(code):
    # Quitar los tres backticks al principio y al final del bloque de código
    return re.sub(r'^\s*```(?:.*\n)?|(?:\n)?```\s*$', '', code, flags=re.DOTALL)

def remove_md_quote_prefix(quote):
    # Quitar el símbolo de cita (>) al principio de cada línea en el bloque de texto
    return re.sub(r'^\s*> ?', '', quote, flags=re.MULTILINE)

def remove_md_unordered_list_prefix(ulist):
    # Quitar el guión o asterisco al principio de cada elemento de la lista
    return re.sub(r'^\s*[-*]\s+', '', ulist, flags=re.MULTILINE)

def remove_md_ordered_list_prefix(olist):
    # Quitar el número seguido de un punto al principio de cada elemento de la lista
    return re.sub(r'^\s*\d+\.\s+', '', olist, flags=re.MULTILINE)

class MDBlock:      # Markdown Block

    def __init__(self, block):
        # Check for empty blocks
        if block is None or block == "":
            raise Exception("Invalid text block: empty or none")
        self.type = block_to_block_type(block)
        clean_block = mdstrip(block, self.type)
        self.nodes = text_to_textnodes(clean_block)

    def __eq__(self, block):
        cond1 = self.type == block.type
        cond2 = self.nodes == block.nodes
        return (cond1 and cond2)
    
    def __repr__(self):
        str = f"Type:{self.type}\n"
        if self.nodes == None:
            str += "No children\n"
        else:
            str += f"Nodes:{len(self.nodes)}"
            for node in self.children:
                str=f"* Node: {node}\n"
        return str
        
    def to_html_node(self):
        if self.nodes is not None:
            html_tag = get_html_tag(self.type)
            children = [textnode_to_html_node(node) for node in self.nodes]
            return ParentNode(html_tag, children)