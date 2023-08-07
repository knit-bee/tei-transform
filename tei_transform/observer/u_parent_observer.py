from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import (
    change_element_tag,
    create_new_element,
    merge_text_content,
)


class UParentObserver(AbstractNodeObserver):
    """
    Observer for <u/> elements with <p/> parent.

    Find <u/> elements with <p/> parent and change tag of parent to <div/>.
    If the parent contains text, a new <p/> is added as first child and
    the text is added to it. If the <u/> element contains a tail, it is
    concatenated with its text content or, if present, added to the tail
    of its last child.
    If the <u/> element is empty, it is removed instead.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "u":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "p":
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
        change_element_tag(parent, "div")
        if parent.text is not None and parent.text.strip():
            self._handle_text_of_parent(parent)
        if node.tail is not None and node.tail.strip():
            self._handle_tail_on_element(node)

    def _handle_text_of_parent(self, parent: etree._Element) -> None:
        new_p = create_new_element(parent, "p")
        new_p.text = parent.text
        parent.text = None
        parent.insert(0, new_p)

    def _handle_tail_on_element(self, node: etree._Element) -> None:
        if len(node) == 0:
            node.text = merge_text_content(node.text, node.tail)
        else:
            last_child = node[-1]
            last_child.tail = merge_text_content(last_child.tail, node.tail)
        node.tail = None
