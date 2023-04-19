from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node


class PtrTargetObserver(AbstractNodeObserver):
    """
    Observer for <ptr/> elements with emtpy @target attribute

    Find <ptr/> elements with @target attribute with empty
    value and remove the attribute.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "ptr"
            and node.attrib.get("target", None) == ""
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        remove_attribute_from_node(node, "target")
