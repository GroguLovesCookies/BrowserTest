from typing import List, Dict, Callable


def set_id(element, value: str):
    element.id = value[1:-1]


def set_class(element, classes: str):
    for class_value in classes[1:-1].split(" "):
        element.classes.append(class_value)


class Element:
    attributes_to_functions: Dict[str, Callable] = \
        {"id": set_id, "class": set_class}

    def __init__(self, el_type: str, raw_content: str):
        self.type: str = el_type
        self.raw_content: str = raw_content
        self.parsed_content: List[Element] = []
        self.attributes: Dict[str, str] = {}
        self.id: str = ""
        self.classes: List[str] = []
        self.parent_list: List[Element] = []

    def add_child_element(self, child):
        self.parsed_content.append(child)
        if type(child) != TextElement:
            child.parent_list.extend(self.parent_list)
            child.parent_list.append(self)

    def print(self, tabs: int = 0, attributes: bool = False):
        if attributes:
            print("  "*tabs + repr(self), end=" ")
            print("(", end="")
            for attribute, value in self.attributes.items():
                print(attribute + ": " + value, end=" ")
            print(")")
        else:
            print("  "*tabs + self.type)
        for child in self.parsed_content:
            child.print(tabs + 1, attributes)
    
    def add_attribute(self, attribute, value):
        self.attributes[attribute] = value
        if attribute in Element.attributes_to_functions.keys():
            Element.attributes_to_functions[attribute](self, value)
    
    def __repr__(self) -> str:
        output = self.type
        if self.id != "":
            output += "#" + self.id
        if len(self.classes) > 0:
            output += "." + ".".join(self.classes)
        return output


class TextElement(Element):
    def __init__(self, text: str):
        self.type = "text"
        self.content: str = text

    def print(self, tabs=0, attributes=False):
        print("  "*tabs + self.content)
