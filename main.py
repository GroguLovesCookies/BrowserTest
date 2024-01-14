from html_parser import lexer
from html_parser.css_parser import selector
from html_parser.element import Element
from html_parser.css_parser import css_parser
from html_parser.css_parser import filters


loaded: str = lexer.load("html_parser/samples/sample1.html")
root: Element = lexer.parse(loaded)
root.print(attributes=True)

print(css_parser.tokenize("body>p p"))