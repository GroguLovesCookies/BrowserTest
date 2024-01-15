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
universal_pattern: str = "\*"


patterns: Dict[str, Callable[[Element], bool]] = {
    attr_is: filter_by_attribute_value, 
    attr_starts_with: filter_by_attribute_start, 
    attr_ends_with: filter_by_attribute_end, 
    attr_contains: filter_by_attribute_content, 
    attr_pipe: filter_by_attribute_pipe, 
    attr_existence_pattern: filter_by_attribute_existence,
    class_pattern: filter_by_class, 
    id_pattern: filter_by_id,
    universal_pattern: filter_nothing
}

split_strings: Dict[str, str] = {
    attr_is: "=",
    attr_starts_with: "^=",
    attr_ends_with: "$=",
    attr_contains: "*=",
    attr_pipe: "|="
}

relation_chars: Dict[chr, str] = {
    ">": Token.RELATION_DIRECT_PARENT,
    "+": Token.RELATION_DIRECT_SIBLING,
    "~": Token.RELATION_INDIRECT_SIBLING,
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
        elif char in relation_chars.keys():
            ignore_next_space = True
            i += 1

            if previous_space:
                output[-1].value = relation_chars[char]
            else:
                output.append(Token(Token.TOKEN_SELECTOR, cur_tok_value))
                cur_tok_value = ""
                output.append(Token(Token.TOKEN_RELATION, relation_chars[char]))

            continue
        elif not in_properties:
            cur_tok_value += char
        ignore_next_space = False
        previous_space = False
        i += 1

    if cur_tok_value:
        output.append(Token(Token.TOKEN_SELECTOR, cur_tok_value))
    
    return output


def parse_selector(tokens: str) -> tuple[List[tuple[Callable, tuple]], List[bool]]:
    out: List[tuple[Callable, tuple]] = []
    direct: List[bool] = []
    is_direct: bool = False
    ignore_direct: bool = False

    for i, token in enumerate(tokens):
        part = token.value
        if token.type == token.TOKEN_SELECTOR:
            matched = False
            for pattern, callback in patterns.items():
                match = re.findall(pattern, part)
                if len(match) > 0:
                    matched = True
                    # Handle logic for special selectors
                    out.append(convert_to_callable(pattern, match[0]))
                    break
            if not matched:
                # Handle raw element selector
                out.append((filter_by_element, (part,)))
        elif token.type == token.TOKEN_RELATION:
            direct.append(token.value)
    return out, direct

def convert_to_callable(pattern: str, matched: str) -> tuple[Callable, tuple]:
    callback: Callable = patterns[pattern]
    if pattern == class_pattern or pattern == id_pattern:
        return callback, (matched[1:],)
    elif pattern == attr_existence_pattern:
        return callback, (matched[1:-1],)
    elif pattern == universal_pattern:
        return callback, ()
    else:
        return callback, matched[1:-1].split(split_strings[pattern])