from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import merge_into_parent


class HiChildObserver(AbstractNodeObserver):
    """
    Observer for <p/> elements with <hi/> parent.

    Find <p/> elements that are children of <hi/>
    and strip the <p/> tag. Text, children, and tail
    of the <p/> element will be preserved.
    If the parent contains text and the <p/> also has
    text content, an <lb/> element is added  to separate
    the text parts.
    """

    def observe(self, node: etree._Element) -> bool:
        parent = node.getparent()
        if (
            etree.QName(node).localname == "p"
            and parent is not None
            and etree.QName(parent).localname == "hi"
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        merge_into_parent(node, add_lb=True)
