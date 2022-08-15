from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class DoubleItemObserver(AbstractNodeObserver):
    """
    Observer for <item/> elements that are children of <item/>
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "item":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "item":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
