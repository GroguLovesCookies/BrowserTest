from typing import List, Union


class Element:
    def __init__(self, el_type: str, raw_content: str):
        self.type: str = el_type
        self.raw_content: str = raw_content
        self.parsed_content: List[Element] = []
    
    def parse_content(self):
        # Parse content and add to list
        ...

    def add_child_element(self, child):
        self.parsed_content.append(child)

    def print(self, tabs=0):
        print("    "*tabs + self.type)
        for child in self.parsed_content:
            child.print(tabs + 1)

class TextElement(Element):
    def __init__(self, text: str):
        self.type = "text"
        self.content: str = text

    def print(self, tabs=0):
        print("    "*tabs + self.content)