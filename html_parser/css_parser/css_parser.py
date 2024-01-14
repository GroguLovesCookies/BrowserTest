import re
from typing import List, Callable, Dict
from html_parser.css_parser.filters import *
from html_parser.utilities import smart_split, copy_string


class_pattern: str = "\..+"
id_pattern: str = "#.+"
attr_is: str = "\[[a-zA-Z\-]+=.+\]"
attr_starts_with: str = "\[[a-zA-Z\-]+\^=.+\]"
attr_ends_with: str = "\[[a-zA-Z\-]+\$=.+\]"
attr_contains: str = "\[[a-zA-Z\-]+\*=.+\]"
attr_pipe: str = "\[[a-zA-Z\-]+\|=.+\]"
attr_existence_pattern: str = "\[[a-zA-Z\-]+\]"


patterns: Dict[str, Callable[[Element], bool]] = {
    class_pattern: filter_by_class, 
    id_pattern: filter_by_id, 
    attr_is: filter_by_attribute_value, 
    attr_starts_with: filter_by_attribute_start, 
    attr_ends_with: filter_by_attribute_end, 
    attr_contains: filter_by_attribute_content, 
    attr_pipe: filter_by_attribute_pipe, 
    attr_existence_pattern: filter_by_attribute_existence
}

split_strings: Dict[str, str] = {
    attr_is: "=",
    attr_starts_with: "^=",
    attr_ends_with: "$=",
    attr_contains: "*=",
    attr_pipe: "|="
}


def parse_selector(selector_text: str, root: Element=None) -> tuple[List[Callable[[Element], bool]], List[bool]]:
    out: List[Callable[[Element], bool]] = []
    direct: List[bool] = []
    is_direct: bool = False
    ignore_direct: bool = False

    parts = selector_text.split()
    global part
    for i, part in enumerate(parts):
        matched = False
        for pattern, callback in patterns.items():
            match = re.findall(pattern, part)
            if len(match) > 0:
                matched = True
                # Handle logic for special selectors
                break
        if not matched:
            if part == ">":
                # Handle logic for direct descendant
                is_direct = True
                ignore_direct = True
            else:
                # Handle raw element selector

                # This is an absolutely horrendous solution to the issue. I was unable to find another one.
                # Passing simply "part" into the lambda expression results in every callback in the list
                # using the same pointer: the last value that part was.
                # Assigning these into a temporary list and passing in temps[i] does not work either,
                # likely due to the same issue.
                # The only possibility is to create separate copies for each part value.
                # All of these must be declared global, or recursive_select will be unable to run the
                # lambda expression.
                exec(f"global temp{part}")
                # Part must be global, or this exec will not recognise it.
                exec(f"temp{part} = (part+'.')[:-1]", globals())
                exec(f"out.append(lambda x: filter_by_element(x, css_parser.temp{part}))")
                # This code actually runs (part = "body"):
                # global tempbody
                # tempbody = (part + ".")[:-1]
                # out.append(lambda x: filter_by_element(x, css_parser.tempbody))
        if i > 0 and not ignore_direct:
            # Must update direct descendant array
            direct.append(is_direct)
            is_direct = False
        ignore_direct = False
    return out, direct

def convert_to_callable(pattern: str, matched: str) -> Callable[[Element], bool]:
    callback: Callable = patterns[pattern]
    if pattern == class_pattern or pattern == id_pattern:
        return lambda x: callback(x, matched)
    elif pattern == attr_existence_pattern:
        return lambda x: callback(x, matched[1:-1])
    else:
        return lambda x: callback(x, *matched.split(split_strings[pattern]))