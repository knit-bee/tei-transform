from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class CodeElementObserver(AbstractNodeObserver):
    """
    Observer for <code/> elements that have descendants or <div/>
    as parent.

    Find <code/> elements that have other elements as descendants
    or are themselves directly descending from a <div/> element
    and change their tag to <ab/>.
    N.B.: This might result in a non-valid TEI document, if
    the parent of the former <code/> element was a, for instance
    a <p/> or <ab/> element. Use in combination with DoublePlikeObserver
    to avoid invalid nesting of p-like elements.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "code":
            if len(node) != 0 or etree.QName(node.getparent()).localname == "div":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "ab")
