class HTMLNode:

    def __init__(self, **kwargs):
        # tag init
        if 'tag_str' in kwargs:                     # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
            HTMLNode.tag = kwargs['tag_str']
        else:
            HTMLNode.tag = None
        # value init
        if 'value_str' in kwargs:                   # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
            HTMLNode.value = kwargs['value_str']
        else:
            HTMLNode.value = None
        # childre init
        if 'children' in kwargs:
            HTMLNode.children = kwargs['children']            # A list of HTMLNode objects representing the children of this node
        else:
            HTMLNode.children = None
        # props init        
        if 'props' in kwargs:
            HTMLNode.props = kwargs['props']                  # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        else:
            HTMLNode.props = None

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        props_str = ""
        for kw, value in self.props.items():
            props_str += " "
            props_str += f"{kw}={value}"
        return props_str

    def __repr__(self):
        str = f"Tag:{self.tag}, Value:{self.value}\n"
        if self.children == None:
            str += "No children\n"
        else:
            for child in self.children:
                str=f"* Child: {child}\n"
            str += self.props_to_html
        return str
        