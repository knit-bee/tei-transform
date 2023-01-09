from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class LonelyRowObserver(AbstractNodeObserver):
    """
    Observer for <row/> elements outside <table/>.

    Find <row/> elements that are outside a <table/> element
    and add a new <table/> as parent. Adjacent <row/> elements
    will be added to the same <table/> element. Empty <row/>
    (no children, text, or tail) elements are removed.
    The tail on the <row/> element is added to the new <table/>
    parent (N.B.: This might not be valid TEI if the former
    parent was, for instance, a <div/> element).
    """

    _new_table: Optional[etree._Element] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "row":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname != "table":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        if (
            len(node) == 0
            and (node.text is None or not node.text.strip())
            and (node.tail is None or not node.tail.strip())
        ):
            parent.remove(node)
            return
        prev_sibling = node.getprevious()
        if prev_sibling is None or prev_sibling != self._new_table:
            new_table = create_new_element(node, "table")
            parent.insert(parent.index(node), new_table)
            self._new_table = new_table
        self._new_table.append(node)
        if node.tail is not None and node.tail.strip():
            if self._new_table.tail is None:
                self._new_table.tail = node.tail.strip()
            else:
                self._new_table.tail += f" {node.tail.strip()}"
            node.tail = None
