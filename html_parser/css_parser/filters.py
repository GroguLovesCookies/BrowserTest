from html_parser.element import Element
from html_parser.css_parser import css_parser


# h1; p; br
def filter_by_element(element: Element, target_type: str) -> bool:
    return element.type == target_type

# #heading; #id-value
def filter_by_id(element: Element, target_id: str) -> bool:
    return element.id == target_id

# .class; .style-differently
def filter_by_class(element: Element, desired_class: str) -> bool:
    return desired_class in element.classes

# [attr]; [src]
def filter_by_attribute_existence(element: Element, desired_attribute: str) -> bool:
    return desired_attribute in element.attributes.keys()

# [attr="value"]; [width="100px"]
def filter_by_attribute_value(element: Element, desired_attribute: str, desired_value: str) -> bool:
    return filter_by_attribute_existence(element, desired_attribute) and element.attributes[desired_attribute] == desired_value

# [attr^="value"]; [href^="../"]
def filter_by_attribute_start(element: Element, desired_attribute: str, desired_start: str) -> bool:
    return filter_by_attribute_existence(element, desired_attribute) and element.attributes[desired_attribute].startswith(desired_start[:-1])

# [attr$="value"]; [href$=".css"]
def filter_by_attribute_end(element: Element, desired_attribute: str, desired_end: str) -> bool:
    return filter_by_attribute_existence(element, desired_attribute) and element.attributes[desired_attribute].endswith(desired_end[1:])

# [attr*="value"]; [href*="samples"]
def filter_by_attribute_content(element: Element, desired_attribute: str, desired_content: str) -> bool:
    return filter_by_attribute_existence(element, desired_attribute) and desired_content[1:-1] in element.attributes[desired_attribute]

# [attr|="value"]; [href|="test"]
def filter_by_attribute_pipe(element: Element, desired_attribute: str, desired_start: str) -> bool:
    return filter_by_attribute_value(element, desired_attribute, desired_start) or \
        filter_by_attribute_start(element, desired_attribute, desired_start[:-1] + "-\"")

# *
def filter_nothing(element: Element):
    return True

def filter_by_composed(element: Element, *args):
    for filter in args:
        if not filter[0](element, *filter[1]):
            return False
    return True