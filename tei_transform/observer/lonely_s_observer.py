from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class LonelySObserver(AbstractNodeObserver):
    """
    Observer for <s/> elements with <body/> or <div/> as parent
    """

    def __init__(self) -> None:
        self._new_p: Optional[etree._Element] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "s":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname in {"div", "body"}:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        prev_sibling = node.getprevious()
        if prev_sibling is None or prev_sibling != self._new_p:
            new_p = create_new_element(node, "p")
            insert_index = parent.index(node)
            parent.insert(insert_index, new_p)
            self._new_p = new_p
        self._new_p.append(node)
