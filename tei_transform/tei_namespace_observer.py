from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class TeiNamespaceObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if node.tag == "TEI":
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
