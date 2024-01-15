import json
from typing import Dict, List

properties: Dict = []
inherited_properties: List[str] = []

with open("css_properties.json") as f:
    properties = json.loads(f.read())

for css_property, property_properties in properties.items():
    if property_properties["inherited"]:
        inherited_properties.append(css_property)
