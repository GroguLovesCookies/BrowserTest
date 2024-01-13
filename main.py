from html_parser import lexer
from html_parser.css_parser import selector
from html_parser.element import Element


loaded: str = lexer.load("html_parser/samples/sample1.html")
root: Element = lexer.parse(loaded)
root.print(attributes=True)
print(selector.recursive_select(root, lambda x: selector.filter_by_element(x, "p")))
print(selector.recursive_select(root, lambda x: selector.filter_by_element(x, "h1")))
print(selector.recursive_select(root, lambda x: selector.filter_by_class(x, "emphasise")))
print(selector.recursive_select(root, lambda x: selector.filter_by_id(x, "heading")))
print(selector.recursive_select(root, lambda x: selector.filter_by_id(x, "second-p")))