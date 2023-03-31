from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class AvailabilityTextObserver(AbstractNodeObserver):
    """
    Observer for <availability/> elements that contain text.

    Remove text content and tails from children of <availability/>
    and add as text content of new <p/> elements.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "availability":
            if node.text is not None and node.text.strip():
                return True
            if [
                child for child in node if child.tail is not None and child.tail.strip()
            ] != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if node.text is not None and node.text.strip():
            self._remove_text_content(node)
        for child in node:
            if child.tail is not None and child.tail.strip():
                self._remove_tail(child)

    def _remove_tail(self, sub_node: etree._Element) -> None:
        new_p = create_new_element(sub_node, "p")
        new_p.text = sub_node.tail.strip()
        sub_node.tail = None
        sub_node.addnext(new_p)

    def _remove_text_content(self, node: etree._Element) -> None:
        new_p = create_new_element(node, "p")
        new_p.text = node.text.strip()
        node.text = None
        node.insert(0, new_p)
