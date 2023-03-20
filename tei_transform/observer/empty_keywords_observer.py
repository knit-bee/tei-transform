from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class EmptyKeywordsObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "keywords" and len(node) == 0:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
