class TextNode:

    def __init__(self, text, text_type, url):
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