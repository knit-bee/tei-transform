from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag, merge_into_parent


class FwChildObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <list/> elements with <fw/> parent.
    """

    def observe(self, node: etree._Element) -> bool:
        target_tags = {"p", "list"}
        if (
            etree.QName(node).localname in target_tags
            and etree.QName(node.getparent()).localname == "fw"
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if etree.QName(node).localname == "p":
            merge_into_parent(node)
        if etree.QName(node).localname == "list":
            change_element_tag(node.getparent(), "ab")
