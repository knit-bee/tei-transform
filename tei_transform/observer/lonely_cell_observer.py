from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class LonelyCellObserver(AbstractNodeObserver):
    """
    Observer for <cell/> elements outside <row/>.
    """

    _new_row: Optional[etree._Element] = None
    _new_table: Optional[etree._Element] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "cell":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname not in {
                "cell",
                "row",
            }:
                return True
            pass
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
