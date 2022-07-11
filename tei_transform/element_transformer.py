from typing import Optional

from lxml import etree


class ElementTransformer:
    def remove_attribute_from_node(
        self, node: etree._Element, attribute: str, namespace: Optional[str] = None
    ) -> None:
        if namespace:
            xml_ns = node.nsmap[namespace]
            attribute = etree.QName(xml_ns, attribute)
        node.attrib.pop(attribute, None)

    def add_namespace_prefix_to_attribute(
        self, node: etree._Element, old_attr: str, namespace: str
    ) -> None:
        old_attribute = node.attrib.get(old_attr)
        if old_attribute is not None:
            attr_value = node.attrib.pop(old_attr)
            new_attribute = etree.QName(namespace, old_attr)
            node.set(new_attribute, attr_value)
