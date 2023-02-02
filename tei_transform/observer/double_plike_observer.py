from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import merge_into_parent


class DoublePlikeObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <ab/> elements with parent <p/> or <ab/>.

    Find <p/> and <ab/> elements that have <p/> or <ab/> as parent
    and strip the inner tag (text and tail as well as the children
    of the inner element will be preserved).
    """

    def observe(self, node: etree._Element) -> bool:
        p_like_tags = {"p", "ab"}
        if etree.QName(node).localname in p_like_tags:
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname in p_like_tags:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        merge_into_parent(node)
