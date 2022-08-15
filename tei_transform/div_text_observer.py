from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class DivTextObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "div" and node.text is not None:
            if node.text.strip():
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
