from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class HiChildObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        parent = node.getparent()
        if (
            etree.QName(node).localname == "p"
            and parent is not None
            and etree.QName(parent).localname == "hi"
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
