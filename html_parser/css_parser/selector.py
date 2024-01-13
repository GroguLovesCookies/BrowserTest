from html_parser.element import Element, TextElement
from typing import List, Callable


def filter_by_element(element: Element, target_type: str) -> bool:
    return element.type == target_type


def filter_by_id(element: Element, target_id: str) -> bool:
    return element.id == target_id


def filter_by_class(element: Element, desired_class: str) -> bool:
    return desired_class in element.classes


def recursive_select(root: Element, condition: Callable[[Element], bool]) -> List[Element]:
    output: List[Element] = []
    if condition(root):
        output.append(root)
    for element in root.parsed_content:
        if type(element) != TextElement:
            output.extend(recursive_select(element, condition))
    
    return output
