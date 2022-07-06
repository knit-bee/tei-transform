from typing import Optional

from lxml import etree


class ElementTransformer:
    def remove_attribute_from_node(
        self, node: etree._Element, attribute: str, namespace: Optional[str] = None
    ) -> None:
        if namespace:
            xml_ns = node.nsmap[namespace]
            attribute = f"{{{xml_ns}}}{attribute}"
        node.attrib.pop(attribute, None)
