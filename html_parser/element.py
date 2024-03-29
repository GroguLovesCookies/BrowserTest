from typing import List, Dict, Callable
from html_parser.css_parser.load_properties import *


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
        self.index: int = 0
        self.style: Dict[str, str] = {}

    @property
    def siblings(self) -> List:
        return self.parent.parsed_content

    @property
    def parent(self):
        return self.parent_list[-1]

    @property
    def next_sibling(self) -> List:
        for i in range(self.index+1, len(self.siblings)):
            if type(self.siblings[i]) != TextElement:
                return self.siblings[i]

    @property
    def siblings_after(self) -> List:
        return self.siblings[self.index+1:]

    def add_child_element(self, child):
        self.parsed_content.append(child)
        if type(child) != TextElement:
            child.parent_list.extend(self.parent_list)
            child.parent_list.append(self)
            child.index = len(self.parsed_content) - 1

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

    def set_style_property(self, css_property: str, css_value: str, ignore_if_existent: bool = False):
        if not (ignore_if_existent and css_property in self.style.keys()):
            self.style[css_property] = css_value
        if type(self) == TextElement:
            return
        if css_property in inherited_properties:
            for child in self.parsed_content:
                child.set_style_property(css_property, css_value, True)


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
        self.style: Dict[str, str] = {}

    def print(self, tabs=0, attributes=False):
        print("  "*tabs + self.content)
    
    def __repr__(self) -> str:
        return self.content


def get_text_elements(root: Element) -> List[TextElement]:
    output: List[TextElement] = []

    if type(root) == TextElement:
        output.append(root)
    else:
        for child in root.parsed_content:
            output.extend(get_text_elements(child))

    return output