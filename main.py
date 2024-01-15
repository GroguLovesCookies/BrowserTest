from html_parser import lexer
from html_parser.css_parser import selector
from html_parser.element import Element, get_text_elements
from html_parser.css_parser import css_parser
from html_parser.css_parser import filters
from html_parser.css_parser.token import Token


loaded: str = lexer.load("html_parser/samples/sample1.html")
root: Element = lexer.parse(loaded)
root.print(attributes=True)

tokens = css_parser.tokenize("p { font-size: 20px; } body { font-size: 40px; }")
zipped_tokens = css_parser.zip_tokens(tokens)
print(zipped_tokens)
for condition, properties in css_parser.parse_zipped_tokens(zipped_tokens):
    for element in selector.filter_by_targeted_selector(root, *condition):
        for css_property, css_value in properties.items():
            element.set_style_property(css_property, css_value)


for element in get_text_elements(root):
    print(element, element.style)
