from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element, merge_into_parent


class HeadChildObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <ab/> elements with <head/> parent.

    Find <p> or <ab/> elements that are children of <head/> and
    remove the target tag. Text, children, and tail of the target
    will not be removed.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname in {"p", "ab"}:
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "head":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        merge_into_parent(node)
