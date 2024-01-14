import re
from typing import List, Callable, Dict
from html_parser.css_parser.filters import *
from html_parser.utilities import smart_split, copy_string
from html_parser.css_parser.token import Token


class_pattern: str = "\.[a-zA-Z\-]+"
id_pattern: str = "#[a-zA-Z\-]+"
attr_is: str = "\[[a-zA-Z\-]+=.+\]"
attr_starts_with: str = "\[[a-zA-Z\-]+\^=.+\]"
attr_ends_with: str = "\[[a-zA-Z\-]+\$=.+\]"
attr_contains: str = "\[[a-zA-Z\-]+\*=.+\]"
attr_pipe: str = "\[[a-zA-Z\-]+\|=.+\]"
attr_existence_pattern: str = "\[[a-zA-Z\-]+\]"


patterns: Dict[str, Callable[[Element], bool]] = {
    attr_is: filter_by_attribute_value, 
    attr_starts_with: filter_by_attribute_start, 
    attr_ends_with: filter_by_attribute_end, 
    attr_contains: filter_by_attribute_content, 
    attr_pipe: filter_by_attribute_pipe, 
    attr_existence_pattern: filter_by_attribute_existence,
    class_pattern: filter_by_class, 
    id_pattern: filter_by_id 
}

split_strings: Dict[str, str] = {
    attr_is: "=",
    attr_starts_with: "^=",
    attr_ends_with: "$=",
    attr_contains: "*=",
    attr_pipe: "|="
}


def tokenize(text: str) -> List[Token]:
    i: int = 0
    output: List[Token] = []
    cur_tok_value: str = ""
    previous_space: bool = False
    ignore_next_space: bool = False

    in_properties: bool = False
    while i < len(text):
        char: chr = text[i]
        # Evaluate the characters
        if char.isspace():
            if not in_properties and cur_tok_value and not ignore_next_space:
                output.append(Token(Token.TOKEN_SELECTOR, cur_tok_value))
                cur_tok_value = ""

                output.append(Token(Token.TOKEN_RELATION, Token.RELATION_INDIRECT_PARENT))

            previous_space = True
            i += 1
            continue
        elif char == ">":
            ignore_next_space = True
            i += 1

            if previous_space:
                output[-1].value = Token.RELATION_DIRECT_PARENT
            else:
                output.append(Token(Token.TOKEN_SELECTOR, cur_tok_value))
                cur_tok_value = ""
                output.append(Token(Token.TOKEN_RELATION, Token.RELATION_DIRECT_PARENT))

            continue
        elif not in_properties:
            cur_tok_value += char
        ignore_next_space = False
        previous_space = False
        i += 1

    if cur_tok_value:
        output.append(Token(Token.TOKEN_SELECTOR, cur_tok_value))
    
    return output


def parse_selector(tokens: str) -> tuple[List[Callable[[Element], bool]], List[bool]]:
    out: List[Callable[[Element], bool]] = []
    direct: List[bool] = []
    is_direct: bool = False
    ignore_direct: bool = False

    global part
    for i, token in enumerate(tokens):
        part = token.value
        if token.type == token.TOKEN_SELECTOR:
            matched = False
            for pattern, callback in patterns.items():
                match = re.findall(pattern, part)
                if len(match) > 0:
                    matched = True
                    # Handle logic for special selectors
                    convert_to_callable(pattern, match[0], out)
                    break
            if not matched:
                # Handle raw element selector

                # This is an absolutely horrendous solution to the issue. I was unable to find another one
                # that still enables using lambda expressions as filters, which is a useful property to have.
                # Passing simply "part" into the lambda expression results in every callback in the list
                # using the same pointer: the last value that part was.
                # Assigning these into a temporary list and passing in temps[i] does not work either,
                # likely due to the same issue.
                # The only possibility is to create separate copies for each part value.
                # All of these must be declared global, or recursive_select will be unable to run the
                # lambda expression.
            # Handle logic for direct descendant
                exec(f"global temp{part}")
                # All variables used in this exec expression must be declared global.
                exec(f"temp{part} = (part+'.')[:-1]", globals())
                exec(f"out.append(lambda x: filter_by_element(x, css_parser.temp{part}))")
                # This code actually runs (when part = "body"):
                # global tempbody
                # tempbody = (part + ".")[:-1]
                # out.append(lambda x: filter_by_element(x, css_parser.tempbody))
        elif token.type == token.TOKEN_RELATION:
            direct.append(part == Token.RELATION_DIRECT_PARENT)
    return out, direct

def convert_to_callable(pattern: str, matched: str, out: List[Callable[[Element], bool]]):
    callback: Callable = patterns[pattern]
    global global_matched, global_pattern
    global_matched = matched
    global_pattern = pattern

    exec(f"global desired_callback_{len(out)}")
    exec(f"desired_callback_{len(out)} = patterns[global_pattern]", globals())
    if pattern == class_pattern or pattern == id_pattern:
        exec(f"global temp{len(out)}")
        exec(f"temp{len(out)} = global_matched[1:]", globals())
        exec(f"out.append(lambda x: css_parser.desired_callback_{len(out)}(x, css_parser.temp{len(out)}))")
    elif pattern == attr_existence_pattern:
        exec(f"global temp{len(out)}")
        exec(f"temp{len(out)} = global_matched[1:-1]", globals())
        exec(f"out.append(lambda x: css_parser.desired_callback_{len(out)}(x, css_parser.temp{len(out)}))")
    else:
        exec(f"global temp{len(out)}")
        exec(f"temp{len(out)} = global_matched[1:-1].split(split_strings[global_pattern])", globals())
        exec(f"out.append(lambda x: css_parser.desired_callback_{len(out)}(x, *css_parser.temp{len(out)}))")