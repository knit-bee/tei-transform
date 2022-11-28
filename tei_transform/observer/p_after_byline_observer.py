from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class PAfterBylineObserver(AbstractNodeObserver):
    """
    Find <byline> elements that have a <p> element as direct sibling.

    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "byline":
            sibling = node.getnext()
            if sibling is not None and etree.QName(sibling).localname == "p":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
