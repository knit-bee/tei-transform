from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class DivTailObserver(AbstractNodeObserver):
    """
    Observer for <div/> elements with tail.

    Find <div/> elements that have tail and add tail as
    text content of a new <p/> that is added as last
    child of the <div/> element.
    N.B.: Use in combination with DivSiblingObserver
    to avoid invalid tree, e.g. if the target <div/>
    contains other <div/> elements.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "div" and (
            node.tail is not None and node.tail.strip()
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        new_p = create_new_element(node, "p")
        new_p.text = node.tail
        node.tail = None
        node.append(new_p)
