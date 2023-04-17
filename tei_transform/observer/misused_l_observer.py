from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class MisusedLObserver(AbstractNodeObserver):
    """
    Observer for <l/> elements with <s/> parent
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "l":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "s":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
