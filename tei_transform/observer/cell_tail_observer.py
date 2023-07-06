from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import merge_text_content


class CellTailObserver(AbstractNodeObserver):
    """
    Observer for <cell/> elements with tail
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "cell" and (
            node.tail is not None and node.tail.strip()
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if len(node) == 0:
            node.text = merge_text_content(node.text, node.tail)
        else:
            last_child = node[-1]
            last_child.tail = merge_text_content(last_child.tail, node.tail)
        node.tail = None
