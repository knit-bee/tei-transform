from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node


class TeiHeaderTypeObserver(AbstractNodeObserver):
    """
    Observer for <teiHeader/>

    Find 'type' attribute in <teiHeader> element and remove it.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node.tag).localname == "teiHeader" and "type" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        remove_attribute_from_node(node, "type")
