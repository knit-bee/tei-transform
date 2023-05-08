from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class HeadParentObserver(AbstractNodeObserver):
    """
    Observer for <head/> elements with wrong parent.

    Find <head/> elements that have <p/>, <ab/>, <head/>, <hi/> or
    <item/> as parent and change their tag to <hi/>.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "head":
            parent = node.getparent()
            if etree.QName(parent).localname in {"p", "ab", "head", "hi", "item"}:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "hi")
