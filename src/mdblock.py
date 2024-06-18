from textnode import text_to_textnodes
import re

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered list"

def block_to_block_type(markdown):
    block = block.strip()
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
        if not re.match(r'^{i}\. '.format(i=i), line):
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
        self.type = block_to_block_type(block)
        clean_block = mdstrip(block, self.type)
        self.nodes = text_to_textnodes(clean_block)
        
