from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class RowChildObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "p":
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "row":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
