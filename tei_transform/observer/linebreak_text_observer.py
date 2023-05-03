from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import merge_text_content


class LinebreakTextObserver(AbstractNodeObserver):
    """
    Observer for <lb/> elements that contain text.

    Remove text content of <lb/> and merge with tail.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "lb"
            and node.text is not None
            and node.text.strip()
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        new_tail = merge_text_content(node.text, node.tail)
        node.text = None
        node.tail = new_tail
