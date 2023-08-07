from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import (
    change_element_tag,
    create_new_element,
    merge_text_content,
)


class ListTextObserver(AbstractNodeObserver):
    """
    Observer for <list/> elements that contain text.

    Find <list/> elements that contain text and add the text
    under a new <item/> element or have any <item/> elements
    with tail as children and concatenate the tail with the
    text content of the <item/>.
    If the <list/> contains <lb/> elements, the <lb/> is
    appended to its previous sibling.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "list":
            if node.text is not None and node.text.strip():
                return True
            # check if any <item/> has tail
            if [
                child for child in node if child.tail is not None and child.tail.strip()
            ] != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if node.text is not None and node.text.strip():
            self._remove_text_content_from_list(node)
        for child in node.iterchildren():
            if child.tail is not None and child.tail.strip():
                if etree.QName(child).localname == "item":
                    self._remove_tail_from_item_child(child)
                if etree.QName(child).localname == "lb":
                    self._handle_lb_child(node, child)

    def _remove_text_content_from_list(self, node: etree._Element) -> None:
        new_item = create_new_element(node, "item")
        new_item.text = node.text.strip()
        node.text = None
        node.insert(0, new_item)

    def _remove_tail_from_item_child(self, item_child: etree._Element) -> None:
        if len(item_child) != 0:
            last_subchild = item_child[0]
            last_subchild.tail = merge_text_content(last_subchild.tail, item_child.tail)
        else:
            item_child.text = merge_text_content(item_child.text, item_child.tail)
        item_child.tail = None

    def _handle_lb_child(self, node: etree._Element, lb_child: etree._Element) -> None:
        prev_sibling = lb_child.getprevious()
        if prev_sibling is None:
            change_element_tag(lb_child, "item")
            lb_child.text, lb_child.tail = lb_child.tail, None
            return
        prev_sibling.append(lb_child)
