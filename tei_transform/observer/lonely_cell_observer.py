from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element, merge_text_content


class LonelyCellObserver(AbstractNodeObserver):
    """
    Observer for <cell/> elements outside <row/>.

    Find <cell/> elements that are outside of a <row/> and
    wrap them with <row/> (and <table/>, if necessary).
    """

    def __init__(self) -> None:
        self._new_row: Optional[etree._Element] = None
        self._new_table: Optional[etree._Element] = None

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
        parent = node.getparent()
        prev_sibling = node.getprevious()
        node_index = parent.index(node)
        if prev_sibling is None or (
            prev_sibling != self._new_row and prev_sibling != self._new_table
        ):
            new_row = create_new_element(node, "row")
            parent.insert(node_index, new_row)
            self._new_row = new_row
        assert self._new_row is not None
        self._new_row.append(node)
        if etree.QName(parent).localname != "table":
            if self._new_table is None or self._new_row not in self._new_table:
                new_table = create_new_element(node, "table")
                parent.insert(node_index, new_table)
                new_table.append(self._new_row)
                self._new_table = new_table
                parent = new_table
        if node.tail is not None and node.tail.strip():
            self._handle_tail_on_item_element(node)

    def _handle_tail_on_item_element(self, node: etree._Element) -> None:
        if len(node) != 0:
            last_child = node[-1]
            last_child.tail = merge_text_content(last_child.tail, node.tail)
        else:
            node.text = merge_text_content(node.text, node.tail)
        node.tail = None
