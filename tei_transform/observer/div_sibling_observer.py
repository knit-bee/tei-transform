from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class DivSiblingObserver(AbstractNodeObserver):
    """
    Observer for invalid siblings of <div/>.

    Find <list/>, <table/>, <quote/>, or <p/> elements that are preceded
    by a <div/> and add a new <div/> as parent for these elements next
    to the preceding <div/>.
    If there are multiple adjacent elements, they will be added
    to the same new <div/>.
    If the element is empty, it will be removed.
    """

    def __init__(self) -> None:
        self._new_div: Optional[etree._Element] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname in {"quote", "table", "list", "p"}:
            if list(node.itersiblings("{*}div", preceding=True)) != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        if (
            len(node) == 0
            and (node.tail is None or not node.tail.strip())
            and (node.text is None or not node.text.strip())
        ):
            parent.remove(node)
            return
        prev_sibling = node.getprevious()
        if prev_sibling is None or prev_sibling != self._new_div:
            new_element = create_new_element(node, "div")
            parent.insert(parent.index(node), new_element)
            self._new_div = new_element
        self._new_div.append(node)
