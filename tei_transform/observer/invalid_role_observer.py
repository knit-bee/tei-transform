from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node


class InvalidRoleObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <div/> with @role attribute.

    Find <p/> and <div/> elements with @role attribute and
    remove the attribute.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname in {"div", "p"}
            and node.attrib.get("role") is not None
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        remove_attribute_from_node(node, "role")
