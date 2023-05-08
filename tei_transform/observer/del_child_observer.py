from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import merge_into_parent


class DelChildObserver(AbstractNodeObserver):
    """
    Observer for <p/>, <ab/>, and <head/> elements with <del/> parent.

    Find <p/>, <ab/>, and <head/> elements that are children of <del/>
    and strip the <p/> tag. Text, children, and tail of the target element
    will not be removed.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname in {"p", "ab", "head"}:
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "del":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        merge_into_parent(node)
