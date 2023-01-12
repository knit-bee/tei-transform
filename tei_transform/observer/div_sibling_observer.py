from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class DivSiblingObserver(AbstractNodeObserver):
    def __init__(self) -> None:
        self._new_div: Optional[etree._Element] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname in {"quote", "table", "list"}:
            if list(node.itersiblings("{*}div", preceding=True)) != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        prev_sibling = node.getprevious()
        if prev_sibling is None or prev_sibling != self._new_div:
            new_element = create_new_element(node, "div")
            parent.insert(parent.index(node), new_element)
            self._new_div = new_element
        self._new_div.append(node)
