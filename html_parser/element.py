from typing import List, Dict


class Element:
    def __init__(self, el_type: str, raw_content: str):
        self.type: str = el_type
        self.raw_content: str = raw_content
        self.parsed_content: List[Element] = []
        self.attributes: Dict[str, str] = {}
    
    def parse_content(self):
        # Parse content and add to list
        ...

    def add_child_element(self, child):
        self.parsed_content.append(child)

    def print(self, tabs: int = 0, attributes: bool = False):
        if attributes:
            print("    "*tabs + self.type, end=" ")
            print("(", end="")
            for attribute, value in self.attributes.items():
                print(attribute + ": " + value, end=" ")
            print(")")
        else:
            print("    "*tabs + self.type)
        for child in self.parsed_content:
            child.print(tabs + 1, attributes)
    
    def add_attribute(self, attribute, value):
        self.attributes[attribute] = value

class TextElement(Element):
    def __init__(self, text: str):
        self.type = "text"
        self.content: str = text

    def print(self, tabs=0, attributes=False):
        print("    "*tabs + self.content)