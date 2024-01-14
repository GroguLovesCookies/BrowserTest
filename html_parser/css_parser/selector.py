from html_parser.element import Element, TextElement
from typing import List, Callable, Dict
from html_parser.css_parser import css_parser

def recursive_select(root: Element, condition: tuple[Callable, tuple], ignore_root: bool = False) -> List[Element]:
    output: List[Element] = []
    if not ignore_root and condition[0](root, *condition[1]):
        output.append(root)
    for element in root.parsed_content:
        if type(element) != TextElement:
            output.extend(recursive_select(element, condition))
    
    return output


def select_from_list(elements: List[Element], condition: tuple[Callable, tuple]) -> List[Element]:
    output = []
    for element in elements:
        if condition[0](element, *condition[1]):
            output.append(element)
    return output


def filter_by_selector_chain(root: Element, selectors: List[tuple[Callable, tuple]], selectors_are_direct: List[bool]) -> List[Element]:
    current_iteration: List[Element] = recursive_select(root, selectors[0])
    temp: List[Element] = []
    for i, selector in enumerate(selectors[1:]):
        if selectors_are_direct[i]:
            for element in current_iteration:
                temp.extend(select_from_list(element.parsed_content, selector))
        else:
            for element in current_iteration:
                temp.extend(recursive_select(element, selector, True))
        current_iteration = temp[:]
        temp = []
    return current_iteration