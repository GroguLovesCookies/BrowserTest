from html_parser import lexer
from html_parser.css_parser import selector
from html_parser.element import Element
from html_parser.css_parser import css_parser
from html_parser.css_parser import filters
from html_parser.css_parser.token import Token


loaded: str = lexer.load("html_parser/samples/sample1.html")
root: Element = lexer.parse(loaded)
root.print(attributes=True)

print(selector.filter_by_targeted_selector(root, [(filters.filter_by_element, ("body",)), (filters.filter_by_element, ("p",)), (filters.filter_by_element, ("p"))],
[Token.RELATION_INDIRECT_PARENT, Token.RELATION_DIRECT_PARENT, Token.RELATION_DIRECT_PARENT], 2))
