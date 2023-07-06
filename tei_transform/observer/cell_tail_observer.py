from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


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
        pass
