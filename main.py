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
print(selector.recursive_select(root, lambda x: selector.filter_by_attribute_existence(x, "href")))
print(selector.recursive_select(root, lambda x: selector.filter_by_attribute_value(x, "width", "\"100px\"")))
print(selector.recursive_select(root, lambda x: selector.filter_by_attribute_start(x, "href", "\"../\"")))
print(selector.recursive_select(root, lambda x: selector.filter_by_attribute_end(x, "href", "\".html\"")))
print(selector.recursive_select(root, lambda x: selector.filter_by_attribute_content(x, "href", "\"samples\"")))
print(selector.recursive_select(root, lambda x: selector.filter_by_attribute_pipe(x, "title", "\"test\"")))
print(selector.filter_by_selector_chain(root, 
[lambda x: selector.filter_by_element(x, "body"), lambda x: selector.filter_by_element(x, "p"), lambda x: selector.filter_by_element(x, "p")],
[True, True]))
