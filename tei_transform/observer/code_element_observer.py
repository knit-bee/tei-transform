from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class CodeElementObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "code":
            if len(node) != 0 or etree.QName(node.getparent()).localname == "div":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
