from typing import Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element, merge_text_content


class LonelyItemObserver(AbstractNodeObserver):
    """
    Observer for <item/> elements outside <list/> elements.
    """

    def __init__(self) -> None:
        self._new_list: Optional[etree._Element] = None

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "item" and etree.QName(
            node.getparent()
        ).localname not in {"item", "list"}:
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
        if prev_sibling is None or prev_sibling != self._new_list:
            new_list = create_new_element(node, "list")
            parent.insert(parent.index(node), new_list)
            self._new_list = new_list
        self._new_list.append(node)
        if node.tail is not None and node.tail.strip():
            self._move_tail_of_item(node)

    def _move_tail_of_item(self, node: etree._Element) -> None:
        if len(node) != 0:
            last_subchild = node[-1]
            last_subchild.tail = merge_text_content(last_subchild.tail, node.tail)
        else:
            node.text = merge_text_content(node.text, node.tail)
        node.tail = None
