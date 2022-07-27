from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import (
    add_namespace_prefix_to_attribute,
    remove_attribute_from_node,
)


class IdAttributeObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if "id" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        qname = etree.QName(node.tag)
        if qname.localname == "TEI":
            remove_attribute_from_node(node, "id")
        else:
            add_namespace_prefix_to_attribute(
                node, "id", "http://www.w3.org/XML/1998/namespace"
            )
