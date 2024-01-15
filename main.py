from html_parser import lexer
from html_parser.css_parser import selector
from html_parser.element import Element
from html_parser.css_parser import css_parser
from html_parser.css_parser import filters
from html_parser.css_parser.token import Token


loaded: str = lexer.load("html_parser/samples/sample1.html")
root: Element = lexer.parse(loaded)
root.print(attributes=True)

tokens = css_parser.tokenize("&p + div")
print(tokens)
conditions, relations, targeted_index = css_parser.parse_selector(tokens)
print(selector.filter_by_targeted_selector(root, conditions, relations, targeted_index))
