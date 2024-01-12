from typing import List
from element import Element


# Load a file into a parseable format
def load(filepath: str, split_lines: bool = True) -> str:
    with open(filepath) as f:
        if not split_lines:
            return f.read()
        lines = []
        for line in f.readlines():
            lines.append(line.strip())
        return "".join(lines)


# Parse loaded file
def parse(loaded: str) -> Element:
    root: Element = Element("root", loaded)
    element_stack: List[str] = []
    root_stack: List[Element] = [root]
    reading_element: bool = False
    current_element: str = ""
    current_element_instance: Element = None

    for i, char in enumerate(loaded): 
        if char == "<":
            reading_element = True
        elif char == ">":
            reading_element = False
            if current_element.startswith("/"):
                if element_stack[-1] != current_element[1:]:
                    return None
                element_stack.pop(-1)
                root_stack.pop(-1)
            else:
                element_stack.append(current_element)
                current_element_instance = Element(current_element, "")
                root_stack[-1].add_child_element(current_element_instance)
                root_stack.append(current_element_instance)
            current_element = ""
        elif reading_element:
            current_element += char

    return root
    

loaded: str = load("html_parser/samples/sample1.html")
root: Element = parse(loaded)
root.print()