from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class UParentObserver(AbstractNodeObserver):
    """
    Observer for <u/> elements with <p/> parent.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "u":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "p":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
