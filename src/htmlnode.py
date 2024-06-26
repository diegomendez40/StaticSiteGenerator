class HTMLNode:

    def __init__(self, tag_str=None, value_str=None, children=None, props=None):
        self.tag = tag_str                              # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value_str                          # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children                        # A list of HTMLNode objects representing the children of this node
        self.props = props if props is not None else {} # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        props_str = ""
        for kw, value in self.props.items():
            props_str += " "
            props_str += f'''{kw}="{value}"'''
        return props_str

    def __eq__(self, node):
        cond1 = self.tag == node.tag
        cond2 = self.value == node.value
        cond3 = self.children == node.children
        return (cond1 and cond2 and cond3)

    def __repr__(self):
        str = f"Tag:{self.tag}, Value:{self.value}\n"
        if self.children == None:
            str += "No children\n"
        else:
            for child in self.children:
                str=f"* Child: {child}\n"
            str += self.props_to_html()
        return str
    
class LeafNode(HTMLNode):                   # An HTMLNode with no children

    def __init__(self, tag_str=None, value_str=None, props=None):
        super().__init__(tag_str, value_str, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All LeafNodes require a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):                  # An HTMLNode with children

    def __init__(self, tag_str, children, props=None):
        super().__init__(tag_str, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All ParentNodes require a tag")
        if self.children == None or self.children == {}:
            raise ValueError("All ParentNodes require children")
        html = f"<{self.tag}>"
        for node in self.children:
            html += node.to_html()
        html += f"</{self.tag}>"
        return html