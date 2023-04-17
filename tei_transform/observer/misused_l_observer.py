from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class MisusedLObserver(AbstractNodeObserver):
    """
    Observer for <l/> elements with <s/> parent

    Find <l/> elements that are children of <s/> and
    change their tag to <w/>.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "l":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "s":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "w")
