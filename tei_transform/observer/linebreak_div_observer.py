from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class LinebreakDivObserver(AbstractNodeObserver):
    """
    Observer for <lb/> elements with tail and <div/> parent.

    Find <lb/> elements with tail that are children of <div/>
    and add a new <p/> wrapping the <lb/> at the index of <lb/>.
    Multiple adjacent <lb/> elements are added to the same <p/>
    element.
    """

    def __init__(self) -> None:
        self._new_p: Optional[etree._Element] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "lb" and etree.QName(
            node.getparent()
        ).localname in {"div", "body"}:
            if node.tail is not None and node.tail.strip():
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        prev_sibling = node.getprevious()
        if prev_sibling is None or prev_sibling != self._new_p:
            new_p = create_new_element(node, "p")
            parent = node.getparent()
            parent.insert(parent.index(node), new_p)
            self._new_p = new_p
        self._new_p.append(node)
